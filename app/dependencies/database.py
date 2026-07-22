from collections.abc import AsyncGenerator
from app.core.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator:

    async with AsyncSessionLocal() as session:
        yield session



# from app.core.database import SessionLocal

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
