from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from fastapi import HTTPException, status

async def get_users_service(
        db: AsyncSession,
        login: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
) -> list[User]:
    query = select(User)

    if login is not None:
        query = query.where(User.login == login)

    if email is not None:
        query = query.where(User.email == email)

    if role is not None:
        query = query.where(User.role == role)

    result = await db.execute(query)
    users = result.scalars().all()

    return users

async def get_user_by_id_service(
        db: AsyncSession,
        user_id: int
)-> User | None:
    return await db.get(User, user_id)

async def delete_user_by_id_service(
        db: AsyncSession,
        user_id: int,
        current_user: User
) -> User | None:
    
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить самого себя"
        )

    user = await db.get(User, user_id)

    if user is None:
        return None

    db.delete(user)
    await db.commit()

    return user