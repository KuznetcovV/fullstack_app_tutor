from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.users import UserResponse
from app.models.user import User, UserRole
from app.services.users import delete_user_by_id_service, get_users_service, get_user_by_id_service

router = APIRouter(prefix="/users", tags=["Пользователи"], dependencies=[Depends(get_current_user)])

@router.get("/", 
            response_model=list[UserResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить пользователей",
        )
async def get_users(
    login: str | None = None,
    email: str | None = None,
    role: UserRole | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_users_service(db, login, email, role)

@router.get("/{user_id}",
            response_model=UserResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить юзера по Id")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await get_user_by_id_service(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user

@router.delete("/{user_id}",
               status_code=status.HTTP_200_OK,
               summary="Удаление пользователя по id")
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await delete_user_by_id_service(db, user_id, current_user)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user