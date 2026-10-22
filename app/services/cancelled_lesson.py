from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cancelled_lesson import CancelledLessonCreate
from app.models.lesson import CancelledLesson
from app.services.helpers.lessons import get_lesson_or_404
from app.exceptions.lesson import LessonAlreadyCancelled, LessonDateWeekdayMismatch
from sqlalchemy import select

async def create_cancelled_lesson_service(db: AsyncSession,
                                  cancelled_lesson: CancelledLessonCreate) -> CancelledLesson:

    lesson = await get_lesson_or_404(db=db, lesson_id=cancelled_lesson.lesson_id)

    if cancelled_lesson.lesson_date.weekday() != lesson.day:
        raise LessonDateWeekdayMismatch()

    query = select(CancelledLesson).where(CancelledLesson.lesson_id == cancelled_lesson.lesson_id,
                                                       CancelledLesson.lesson_date == cancelled_lesson.lesson_date)

    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    if existing is not None:
        raise LessonAlreadyCancelled()

    db_cancelled_lesson = CancelledLesson(**cancelled_lesson.model_dump())

    db.add(db_cancelled_lesson)
    await db.commit()
    await db.refresh(db_cancelled_lesson)

    return db_cancelled_lesson