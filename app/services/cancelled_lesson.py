from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cancelled_lesson import CancelledLessonCreate
from app.models.lesson import CancelledLesson

async def create_cancelled_lesson_service(db: AsyncSession,
                                  cancelled_lesson: CancelledLessonCreate) -> CancelledLesson:

    db_cancelled_lesson = CancelledLesson(**cancelled_lesson.model_dump())

    db.add(db_cancelled_lesson)
    await db.commit()
    await db.refresh(db_cancelled_lesson)

    return db_cancelled_lesson