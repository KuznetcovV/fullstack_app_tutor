from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import Lesson
from app.models.student import Student
from app.schemas.lesson import LessonCreate, LessonUpdate
from fastapi import HTTPException, status
from datetime import date

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
    today = date.today().weekday()
    result = await db.execute(select(Lesson).where(Lesson.day == today))
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
    
    db.delete(lesson)
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
