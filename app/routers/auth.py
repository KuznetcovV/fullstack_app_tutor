from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.auth import RegisterRequest, TokenResponse, RefreshRequest
from app.services.auth import register_service, login_service, refresh_service, logout_service
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    return await register_service(db, data)

@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await login_service(
        db,
        data.username,
        data.password
    )

@router.get("/me")
async def me(
    curent_user: User = Depends(get_current_user)
):
    return {
        "id": curent_user.id,
        "login": curent_user.login,
        "role": curent_user.role
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    return await refresh_service(
        db,
        data.refresh_token
    )

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await logout_service(
        db,
        current_user
    )
