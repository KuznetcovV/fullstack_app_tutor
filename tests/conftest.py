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

@pytest_asyncio.fixture
async def created_solo_student_and_lesson(created_solo_student, authorized_client):
    response = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert response.status_code == 201, f"Не удалось создать занятие для фикстуры: {response.text}"
    return response.json()

@pytest_asyncio.fixture
async def created_solo_student_and_many_lessons(created_solo_student, authorized_client):
    first_lesson = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 1,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })
    assert first_lesson.status_code == 201, f"Не удалось создать занятие для фикстуры: {first_lesson.text}"

    second_lesson = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 3,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert second_lesson.status_code == 201, f"Не удалось создать занятие для фикстуры: {second_lesson.text}"

    third_lesson = await authorized_client.post("/lessons/", json={
        "student_id": created_solo_student["id"],
        "day": 5,
        "time_start": "12:00:00",
        "time_end": "13:00:00"
    })

    assert third_lesson.status_code == 201, f"Не удалось создать занятие для фикстуры: {third_lesson.text}"

    return [first_lesson.json(), second_lesson.json(), third_lesson.json()]

LESSON_DAYS = [1, 3, 5]
STUDENT_TIME_SLOTS = [
    ("12:00:00", "13:00:00"),
    ("13:00:00", "14:00:00"),
    ("14:00:00", "15:00:00"),
]

@pytest_asyncio.fixture
async def created_many_students_many_lessons(created_many_students, authorized_client):

    students_lessons = {}

    for student, (time_start, time_end) in zip(created_many_students, STUDENT_TIME_SLOTS):
        lessons = []

        for day in LESSON_DAYS:
            response = await authorized_client.post("/lessons/", json={
                "student_id": student["id"],
                "day": day,
                "time_start": time_start,
                "time_end": time_end
            })
            assert response.status_code == 201, (
                f"Не удалось создать занятие для фикстуры "
                f"(student_id={student['id']}, day={day}): {response.text}"
            )
            lessons.append(response.json())

        students_lessons[student["id"]] = lessons

    return students_lessons

@pytest_asyncio.fixture
async def created_solo_student_and_lesson_log(created_solo_student, authorized_client):
    response = await authorized_client.post("/lesson_logs/", json={
        "student_id": created_solo_student["id"],
        "lesson_log_date": "2026-09-22"
    })

    assert response.status_code == 201, f"Не удалось создать лог занятия для фикстуры: {response.text}"
    return response.json()