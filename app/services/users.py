from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from fastapi import HTTPException, status
from app.services.helpers.user import get_user_or_404


#Получение
#Получение списка пользователей с опциональными параметрами
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

#Получение пользователя по Id
async def get_user_by_id_service(
        db: AsyncSession,
        user_id: int
)-> User:
    user = await get_user_or_404(db=db, user_id=user_id)
    return user

#Удаление пользователя по его Id
async def delete_user_by_id_service(
        db: AsyncSession,
        user_id: int,
        current_user: User
) -> User:

    user = await get_user_or_404(db=db, user_id=user_id)
    
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить самого себя"
        )

    await db.delete(user)
    await db.commit()

    return user