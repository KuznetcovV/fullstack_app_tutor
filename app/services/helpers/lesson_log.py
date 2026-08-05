from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson_log import LessonLog
from app.exceptions.lesson_log import LessonLogNotFound

async def get_lesson_log_or_404(db: AsyncSession, lesson_log_id: int) -> LessonLog:
    lesson_log = await db.get(LessonLog, lesson_log_id)

    if lesson_log is None:
        raise LessonLogNotFound()

    return lesson_log