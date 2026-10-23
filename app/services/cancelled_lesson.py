from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.cancelled_lesson import CancelledLessonCreate
from app.models.lesson import CancelledLesson
from app.models.lesson_log import LessonLog
from app.services.helpers.cancelled_lesson import get_cancelled_lesson_or_404
from app.services.helpers.lessons import get_lesson_or_404
from app.exceptions.lesson import LessonAlreadyCancelled, LessonDateWeekdayMismatch, CancelledLessonHasLessonLog
from sqlalchemy import select

async def create_cancelled_lesson_service(db: AsyncSession,
                                  cancelled_lesson: CancelledLessonCreate) -> CancelledLesson:

    lesson = await get_lesson_or_404(db=db, lesson_id=cancelled_lesson.lesson_id)

    if cancelled_lesson.lesson_date.weekday() != lesson.day:
        raise LessonDateWeekdayMismatch()

    lesson_logs_query = select(LessonLog).where(LessonLog.lesson_id == cancelled_lesson.lesson_id, 
                                                LessonLog.lesson_log_date == cancelled_lesson.lesson_date)
    result = await db.execute(lesson_logs_query)
    existing_log = result.first()
    if existing_log is not None:
        raise CancelledLessonHasLessonLog()

    query = select(CancelledLesson).where(CancelledLesson.lesson_id == cancelled_lesson.lesson_id,
                                                       CancelledLesson.lesson_date == cancelled_lesson.lesson_date)

    result = await db.execute(query)
    existing_cancel = result.scalar_one_or_none()
    if existing_cancel is not None:
        raise LessonAlreadyCancelled()

    db_cancelled_lesson = CancelledLesson(**cancelled_lesson.model_dump())

    db.add(db_cancelled_lesson)
    await db.commit()
    await db.refresh(db_cancelled_lesson)

    return db_cancelled_lesson

async def get_cancelled_lessons_service(db: AsyncSession, 
                                        lesson_id: int | None = None, 
                                        date_from: date | None = None,
                                        date_to: date | None = None) -> list[CancelledLesson]:
    query = select(CancelledLesson)

    if lesson_id is not None:
        query = query.where(CancelledLesson.lesson_id == lesson_id)

    if date_from is not None:
        query = query.where(CancelledLesson.lesson_date >= date_from)

    if date_to is not None:
        query = query.where(CancelledLesson.lesson_date <= date_to)

    result = await db.execute(query.order_by(CancelledLesson.lesson_date, CancelledLesson.id))
    return result.scalars().all()


async def get_cancelled_lesson_by_id_service(db: AsyncSession, cancelled_lesson_id: int) -> CancelledLesson:
    return await get_cancelled_lesson_or_404(db=db, cancelled_lesson_id=cancelled_lesson_id)

async def delete_cancelled_lesson_by_id_service(db: AsyncSession, cancelled_lesson_id: int) -> None:
    cancelled_lesson = await get_cancelled_lesson_or_404(db=db, cancelled_lesson_id=cancelled_lesson_id)

    await db.delete(cancelled_lesson)
    await db.commit()