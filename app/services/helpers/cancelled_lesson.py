from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson import CancelledLesson
from app.exceptions.lesson import CancelledLessonNotFound

async def get_cancelled_lesson_or_404(db: AsyncSession, cancelled_lesson_id: int) -> CancelledLesson:
    cancelled_lesson = await db.get(CancelledLesson, cancelled_lesson_id)

    if cancelled_lesson is None:
        raise CancelledLessonNotFound()

    return cancelled_lesson