from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.lesson_log import LessonLogCreate, LessonLogResponse, LessonLogUpdate
from app.models.lesson_log import LessonLog
from app.models.student import Student
from app.models.lesson import Lesson
from fastapi import HTTPException, status

#Получение
async def get_lesson_log_service(
        db: AsyncSession
) -> list[LessonLog]:
    result = await db.execute(select(LessonLog))
    return result.scalars().all()


async def get_lesson_log_by_id_service(
        db: AsyncSession,
        lesson_log_id: int) -> LessonLog | None:
    return await db.get(LessonLog, lesson_log_id)

#Создание
async def create_lesson_log_service(db: AsyncSession, lesson_log: LessonLogCreate) -> LessonLog:
    student = await db.get(Student, lesson_log.student_id)

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    

    if lesson_log.lesson_id is not None:
        lesson = await db.get(Lesson, lesson_log.lesson_id)
        if lesson is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Занятие не найдено")

    await check_student_lesson_link(db=db, lesson_id=lesson_log.lesson_id, student_id=lesson_log.student_id)

    db_lesson_log = LessonLog(**lesson_log.model_dump())
    db.add(db_lesson_log)
    await db.commit()
    await db.refresh(db_lesson_log)

    return db_lesson_log


#Обновление
async def update_lesson_log_service(db: AsyncSession, lesson_log_id: int, data: LessonLogUpdate) -> LessonLog | None:
    lesson_log = await db.get(LessonLog, lesson_log_id)

    if lesson_log is None:
        return None

    if data.student_id is not None:
        if await db.get(Student, data.student_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")

    if data.lesson_id is not None:
        if await db.get(Lesson, data.lesson_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Занятие не найдено")
        
    lesson_id = data.lesson_id or lesson_log.lesson_id
    student_id = data.student_id or lesson_log.student_id

    await check_student_lesson_link(db=db, lesson_id=lesson_id, student_id=student_id)

    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(lesson_log, key, value)

    await db.commit()
    await db.refresh(lesson_log)

    return lesson_log



#Удаление

async def delete_lesson_log_service(db: AsyncSession, lesson_log_id: int) -> LessonLog | None:
    lesson_log = await db.get(LessonLog, lesson_log_id)
    if lesson_log is None:
        return None
    
    db.delete(lesson_log)
    await db.commit()

    return lesson_log


#Вспомогательные функции
async def check_student_lesson_link(db: AsyncSession, lesson_id: int, student_id: int):
    lesson = await db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Занятие не найдено")

    if lesson.student_id != student_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="У указанного ученика нет такого занятия")