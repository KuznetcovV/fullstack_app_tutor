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

#фикстура для накатывания всех миграций до последней на тестовую бд
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
    assert response.status_code == 200, f"Не удалось зарегистрировать юзера для фикстуры: {response.text}"

    client.headers["Authorization"] = f"Bearer {response.json()["access_token"]}"
    return client

#создание студента
@pytest_asyncio.fixture
async def created_solo_student(authorized_client):
    response = await authorized_client.post("/students/", json={
        "first_name": "Тестовый",
        "last_name": "Студент",
        "number_of_class": 5,
        "phone": "+79990000000",
        "parent_name": "Родитель",
        "parent_phone": "+79990000001",
        "notes": "Тестовые заметки",
        "is_active": True
    })
    assert response.status_code == 201, f"Не удалось создать студента для фикстуры: {response.text}"
    return response.json()

@pytest_asyncio.fixture
async def created_many_students(authorized_client):
    first_sutdent = await authorized_client.post("/students/", json={
        "first_name": "Иван",
        "last_name": "Петров",
        "number_of_class": 9,
        "phone": "+79969133520",
        "parent_name": "Алексей Петров",
        "parent_phone": "89992223344",
        "notes": "Хорошо понимает дроби",
        "is_active": True
    })

    assert first_sutdent.status_code == 201, f"Не удалось создать студента для фикстуры: {first_sutdent.text}"
    
    second_student = await authorized_client.post("/students/", json={
        "first_name": "Мария",
        "last_name": "Сидорова",
        "number_of_class": 10,
        "phone": "89912312312",
        "parent_name": "Елена Сидорова",
        "parent_phone": "89992223344",
        "notes": None,
        "is_active": True
    })

    assert second_student.status_code == 201, f"Не удалось создать студента для фикстуры: {second_student.text}"

    third_student = await authorized_client.post("/students/", json={
        "first_name": "Дмитрий",
        "last_name": "Иванов",
        "number_of_class": 10,
        "phone": None,
        "parent_name": None,
        "parent_phone": None,
        "notes": "Подготовка к ЕГЭ",
        "is_active": False
    })

    assert third_student.status_code == 201, f"Не удалось создать студента для фикстуры: {third_student.text}"

    result_list = [first_sutdent.json(), second_student.json(), third_student.json()]

    return result_list