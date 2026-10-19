from datetime import date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson
from app.schemas.schedule import ScheduleResponse

async def get_schedule_service(
        date_from: date,
        date_to: date | None,
        db: AsyncSession
        ) -> list[ScheduleResponse]:

    response = list()

    if date_to is None:
        date_to = date_from

    query = select(Lesson)
    result = await db.execute(query)
    all_lessons = result.scalars().all()

    current_date = date_from

    while current_date <= date_to:
        weekday = current_date.weekday()

        for lesson in all_lessons:
            if lesson.day == weekday:
                response.append(ScheduleResponse(
                    lesson_id=lesson.id,
                    student_id=lesson.student_id,
                    time_start=lesson.time_start,
                    time_end=lesson.time_end,
                    lesson_date=current_date
                ))

        current_date += timedelta(days=1)

    return response
