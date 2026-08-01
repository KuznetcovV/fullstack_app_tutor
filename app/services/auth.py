from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.core.database import AsyncSession
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)

async def register_service(
        db: AsyncSession,
        data: RegisterRequest
) -> User:
    
    query = select(User).where(User.login == data.login)

    result = await db.execute(query)

    exists = result.scalar_one_or_none()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Логин уже занят"
        )

    if data.email is not None:
        result = await db.execute(
            select(User).where(User.email == data.email)
        )

        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email уже используется"
            )

    user = User(
        login=data.login,
        email = data.email,
        password_hash = hash_password(data.password),
        role=UserRole.STUDENT
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def login_service(
        db: AsyncSession,
        login: str,
        password: str
) -> TokenResponse:

    result = await db.execute(
        select(User).where(User.login == login)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    if not verify_password(
        password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role.value,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id),
        }
    )

    user.refresh_token_hash = hash_password(refresh_token)
    await db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_service(
        db: AsyncSession,
        refresh_token: str
):
    try:
        payload = verify_refresh_token(refresh_token)

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh_token")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = int(user_id)
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")

    if user.refresh_token_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked"
        )

    if not verify_password(refresh_token, user.refresh_token_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    new_access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role.value
        }
    )

    new_refresh_token = create_refresh_token(
        {
            "sub": str(user.id)
        }
    )

    user.refresh_token_hash = hash_password(new_refresh_token)

    await db.commit()

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

async def logout_service(
        db: AsyncSession,
        user: User
):
    user.refresh_token_hash = None
    await db.commit()

    return {
        "message": "Successfully logged out"
    }