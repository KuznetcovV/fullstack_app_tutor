from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.lesson_log import LessonLogCreate, LessonLogUpdate
from app.models.lesson_log import LessonLog
from app.models.lesson import Lesson

from app.exceptions.student import (
    StudentLessonMismatch
    )
from app.exceptions.lesson import LessonNotFound

from app.services.helpers.lesson_log import get_lesson_log_or_404
from app.services.helpers.students import get_student_or_404
from app.services.helpers.lessons import get_lesson_or_404

#Получение
#Получение списка логов занятий
async def get_lesson_log_service(
        db: AsyncSession
) -> list[LessonLog]:
    
    query = await db.execute(select(LessonLog))
    lesson_logs = query.scalars().all()

    return lesson_logs

#Получение лога занятия по его Id
async def get_lesson_log_by_id_service(
        db: AsyncSession,
        lesson_log_id: int
) -> LessonLog | None:

    lesson_log = await get_lesson_log_or_404(db=db, lesson_log_id=lesson_log_id)

    return lesson_log

#Создание
async def create_lesson_log_service(
        db: AsyncSession,
        lesson_log: LessonLogCreate
) -> LessonLog:

    await get_student_or_404(db=db, student_id=lesson_log.student_id)
    
    if lesson_log.lesson_id is not None:
        await get_lesson_or_404(db=db, lesson_id=lesson_log.lesson_id)

    #Проверка, принадлежит ли указанное занятие указанному ученику
    await check_student_lesson_link(db=db, lesson_id=lesson_log.lesson_id, student_id=lesson_log.student_id)

    db_lesson_log = LessonLog(**lesson_log.model_dump())

    db.add(db_lesson_log)
    await db.commit()
    await db.refresh(db_lesson_log)

    return db_lesson_log

#Обновление
async def update_lesson_log_service(db: AsyncSession, lesson_log_id: int, data: LessonLogUpdate) -> LessonLog | None:
    lesson_log = await get_lesson_log_or_404(db=db, lesson_log_id=lesson_log_id)

    if data.student_id is not None:
        await get_student_or_404(db=db, student_id=data.student_id)

    if data.lesson_id is not None:
        await get_lesson_or_404(db=db, lesson_id=data.lesson_id)
        
    lesson_id = data.lesson_id or lesson_log.lesson_id
    student_id = data.student_id or lesson_log.student_id

    #Проверка, принадлежит ли указанное занятие указанному ученику
    await check_student_lesson_link(db=db, lesson_id=lesson_id, student_id=student_id)

    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(lesson_log, key, value)

    await db.commit()
    await db.refresh(lesson_log)

    return lesson_log

#Удаление
async def delete_lesson_log_service(db: AsyncSession, lesson_log_id: int) -> LessonLog | None:

    lesson_log = await get_lesson_log_or_404(db=db, lesson_log_id=lesson_log_id)
    
    await db.delete(lesson_log)
    await db.commit()

#Вспомогательные функции
#Проверка, принадлежит ли указанное занятие указанному ученику
async def check_student_lesson_link(db: AsyncSession, lesson_id: int, student_id: int):

    lesson = await db.get(Lesson, lesson_id)

    if lesson is None:
        raise LessonNotFound()

    if lesson.student_id != student_id:
        raise StudentLessonMismatch()

