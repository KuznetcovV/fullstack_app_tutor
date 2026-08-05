from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lesson import Lesson
from app.exceptions.lesson import LessonNotFound

async def get_lesson_or_404(db: AsyncSession, lesson_id: int) -> Lesson:
    lesson = await db.get(Lesson, lesson_id)

    if lesson is None:
        raise LessonNotFound()

    return lesson