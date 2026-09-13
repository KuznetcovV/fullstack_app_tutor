import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from alembic.config import Config
from alembic import command
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.config import TEST_DATABASE_URL
from app.dependencies.database import get_db

#фикстура для накатывания всех миграций до последней
@pytest.fixture(scope="session", autouse=True)
def aply_migrations():
    cfg = Config("alembic-test.ini")
    command.upgrade(cfg, "head")
    yield

#создание движка, для тестовой бд
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)

#сессия для одного теста обернутая в транзакцию с откатом после 
@pytest_asyncio.fixture
async def db_session():
    async with test_engine.connect() as connection:
        await connection.begin()
        session = AsyncSession(bind=connection, join_transaction_mode="create_savepoint")
        yield session
        await session.close()
        await connection.rollback()

#Http клиент который вместо реальной бд подсовывает db_session
@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

#Фикстура для добавления клиенту аксесс токена
@pytest_asyncio.fixture
async def authorized_client(client):
    response = await client.post("/auth/register", json={
        "login": "test_user",
        "password": "strongpassword123",
    })

    client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"

    return client
