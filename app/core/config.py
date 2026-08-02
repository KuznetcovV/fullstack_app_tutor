import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

FRONTEND_URL = os.getenv("FRONTEND_URL")

TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Europe/Moscow"))

if not FRONTEND_URL:
    raise RuntimeError("FRONTEND_URL is not configured")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)
)