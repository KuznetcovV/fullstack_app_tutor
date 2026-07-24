from enum import IntEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time

from app.models.lesson import Lesson

class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


async def seed_lessons(db: AsyncSession):

    result = await db.execute(select(Lesson).limit(1))
    exists = result.scalar_one_or_none()
    if exists:
        print("Lessons already exists")
        return
    
    lessons = [
        Lesson(
            student_id=1,
            day=Weekday.MONDAY,
            time_start=time(15, 0),
            time_end=time(16, 0)
        ),

        Lesson(
            student_id=2,
            day=Weekday.MONDAY,
            time_start=time(16, 0),
            time_end=time(17, 0)
        ),

        Lesson(
            student_id=3,
            day=Weekday.MONDAY,
            time_start=time(17, 0),
            time_end=time(18, 0)
        ),

        Lesson(
            student_id=4,
            day=Weekday.TUESDAY,
            time_start=time(15, 0),
            time_end=time(16, 0)
        ),
        

        Lesson(
            student_id=1,
            day=Weekday.WEDNESDAY,
            time_start=time(15, 0),
            time_end=time(16, 0)
        ),

        Lesson(
            student_id=4,
            day=Weekday.THURSDAY,
            time_start=time(15, 0),
            time_end=time(16, 0)
        ),

        Lesson(
            student_id=1,
            day=Weekday.FRIDAY,
            time_start=time(15, 0),
            time_end=time(16, 0)
        ),

        Lesson(
            student_id=2,
            day=Weekday.FRIDAY,
            time_start=time(16, 0),
            time_end=time(17, 0)
        ),

        Lesson(
            student_id=3,
            day=Weekday.FRIDAY,
            time_start=time(17, 0),
            time_end=time(18, 0)
        ),

        Lesson(
            student_id=5,
            day=Weekday.TUESDAY,
            time_start=time(16, 0),
            time_end=time(17, 0)
        ),

        Lesson(
            student_id=6,
            day=Weekday.WEDNESDAY,
            time_start=time(18, 0),
            time_end=time(19, 0)
        ),

        Lesson(
            student_id=7,
            day=Weekday.THURSDAY,
            time_start=time(16, 0),
            time_end=time(17, 0)
        ),

        Lesson(
            student_id=8,
            day=Weekday.FRIDAY,
            time_start=time(18, 0),
            time_end=time(19, 0)
        ),

        Lesson(
            student_id=5,
            day=Weekday.MONDAY,
            time_start=time(18, 0),
            time_end=time(19, 0)
        ),

        Lesson(
            student_id=6,
            day=Weekday.TUESDAY,
            time_start=time(18, 0),
            time_end=time(19, 0)
        ),

        Lesson(
            student_id=7,
            day=Weekday.THURSDAY,
            time_start=time(17, 0),
            time_end=time(18, 0)
        ),

        Lesson(
            student_id=8,
            day=Weekday.WEDNESDAY,
            time_start=time(16, 0),
            time_end=time(17, 0)
        ),
    ]

    db.add_all(lessons)

    await db.commit()

    print("Lessons seeded")