from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import Lesson
from app.models.student import Student
from app.schemas.lesson import LessonCreate, LessonUpdate
from fastapi import HTTPException, status
from app.core.time import today

#Получение
async def get_lessons_service(
        day: int | None,
        db: AsyncSession
        ) -> list[Lesson]:
    
    query = select(Lesson)

    if day is not None:
        query = query.where(Lesson.day == day)

    result = await db.execute(query)
    return result.scalars().all()

async def get_lesson_by_id_service(db: AsyncSession, lesson_id: int) -> Lesson | None:
    return await db.get(Lesson, lesson_id)


async def get_today_lesson_service(db: AsyncSession) -> list[Lesson]:
    today_weekday = today().weekday()
    result = await db.execute(select(Lesson).where(Lesson.day == today_weekday))
    lessons = result.scalars().all()
    return lessons

#Создание
async def create_lesson_service(db: AsyncSession, lesson: LessonCreate) -> Lesson:
    student = await db.get(Student, lesson.student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Ученик не найден")
    
    await check_lessons_intersection(db=db, lesson=lesson)

    db_lesson = Lesson(**lesson.model_dump())

    db.add(db_lesson)
    await db.commit()
    await db.refresh(db_lesson)

    return db_lesson

#Обновление
async def update_lesson_service(db: AsyncSession,
                          lesson_id: int,
                          data: LessonUpdate
                          ) -> Lesson | None:
    
    lesson = await db.get(Lesson, lesson_id)

    if lesson is None:
        return None

    if data.student_id is not None:
        student = await db.get(Student, data.student_id)

        if student is None:
            raise HTTPException(status_code=404,
                                detail="Ученик не найден")
    
    update_data = data.model_dump(exclude_unset=True)

    validate_lesson_time(lesson=lesson, data=data)
    

    for field, value in update_data.items():
        setattr(lesson, field, value)

    await check_lessons_intersection(db=db, lesson=lesson, exclude_id=lesson.id)

    await db.commit()
    await db.refresh(lesson)

    return lesson

#Удаление
async def delete_lesson_service(db: AsyncSession,
                          lesson_id: int) -> Lesson | None:
    lesson = await db.get(Lesson, lesson_id)
    if lesson is None:
        return None
    
    await db.delete(lesson)
    await db.commit()

    return lesson


#Вспомогательные функции
async def check_lessons_intersection(db: AsyncSession, lesson: Lesson | LessonCreate, exclude_id: int | None = None):
    query = select(Lesson).where(Lesson.day == lesson.day)

    if exclude_id is not None:
        query = query.where(Lesson.id != exclude_id)

    result = await db.execute(query)
    lessons = result.scalars().all()
    
    for existing in lessons:
        if lesson.time_start < existing.time_end and lesson.time_end > existing.time_start:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Указанное время занятия пересекается с уже существующим")

def validate_lesson_time(lesson: Lesson, data: LessonUpdate):
    if data.time_start is None and data.time_end is None:
        return None

    if data.time_start is None:
        time_start = lesson.time_start
    else:
        time_start = data.time_start

    if data.time_end is None:
        time_end = lesson.time_end
    else:
        time_end = data.time_end

    if time_end <= time_start:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Время начала занятия должно быть раньше времени конца занятия.")

    return