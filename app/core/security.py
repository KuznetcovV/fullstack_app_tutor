from datetime import datetime, timedelta, UTC

import jwt
from pwdlib import PasswordHash

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)

def create_access_token(data: dict) -> str:
    payload = data.copy()

    payload["type"] = "access"

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def verify_access_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    if payload.get("type") != "access":
        raise ValueError("Invalid token type")

    return payload


def create_refresh_token(data: dict) -> str:
    payload = data.copy()

    payload["type"] = "refresh"

    payload["exp"] = (
        datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_refresh_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    if payload.get("type") != "refresh":
        raise ValueError("Invalid token type")

    return payload