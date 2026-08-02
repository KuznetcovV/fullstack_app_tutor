from datetime import datetime
from app.core.config import TIMEZONE

def today():
    return datetime.now(TIMEZONE).date()

def now():
    return datetime.now(TIMEZONE)