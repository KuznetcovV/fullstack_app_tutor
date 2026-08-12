from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.exceptions.user import UserNotFound

async def get_user_or_404(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)

    if user is None:
        raise UserNotFound()

    return user