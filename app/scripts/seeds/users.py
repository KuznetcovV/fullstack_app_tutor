from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.models.user import User, UserRole


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


async def seed_users(db: AsyncSession):
    result = await db.execute(select(User).limit(1))
    exists = result.scalar_one_or_none()

    if exists:
        print("Users already exists")
        return

    users = [
        User(
            login="admin",
            email="admin@test.ru",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
            refresh_token_hash=None
        ),

        User(
            login="ivan",
            email="ivan@test.ru",
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="maria",
            email="maria@test.ru",
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="dmitriy",
            email=None,
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="anton",
            email=None,
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="ekaterina",
            email="katya@test.ru",
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="maksim",
            email="maks@test.ru",
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="alina",
            email=None,
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),

        User(
            login="kirill",
            email="kirill@test.ru",
            password_hash=hash_password("123456"),
            role=UserRole.STUDENT,
            refresh_token_hash=None
        ),
    ]

    db.add_all(users)
    await db.commit()

    print("Users seeded")