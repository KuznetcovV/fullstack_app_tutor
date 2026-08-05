from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.lesson_log import LessonLog
from app.models.subscription import Subscription
from app.schemas.student import StudentCreate, StudentUpdate
from sqlalchemy import func, or_
from app.core.time import today
from app.exceptions.student import (
    StudentAlreadyExists
)

from app.exceptions.lesson import LessonsForStudentNotFound
from app.exceptions.lesson_log import LessonLogForStudentNotFound
from app.exceptions.subscription import (
    SubscriptionActiveNotFound,
    SubscriptionsForStudentNotFound
    )

from app.services.helpers.students import get_student_or_404

#Получение
#Получение учеников с опциональными фильтрами по классу и активности
async def get_students_service(
        db: AsyncSession, 
        number_of_class: int | None, 
        is_active: bool | None
        ) -> list[Student]:
    
    query = select(Student)

    if number_of_class is not None:
        query = query.where(Student.number_of_class == number_of_class)

    if is_active is not None:
        query = query.where(Student.is_active == is_active)

    result = await db.execute(query)
    students = result.scalars().all()

    return students

#Получение списка учеников, имя или фамилия или полное имя совпадает со строкой запроса
async def search_students_service(db: AsyncSession, query: str) -> list[Student]:
    query = select(Student).where(or_(Student.first_name.ilike(f"%{query}%"),
                Student.last_name.ilike(f"%{query}%"),
                func.concat(
                    Student.first_name, " ", Student.last_name
                ).ilike(f"%{query}%")))
    
    result = await db.execute(query)
    students = result.scalars().all()

    return students
    
#Получение ученика по его id
async def get_student_by_id_service(db: AsyncSession, student_id: int) -> Student | None:
    student = await get_student_or_404(db=db, student_id=student_id)

    return student

#Получение списка уроков для ученика
async def get_lessons_for_student_service(db: AsyncSession, student_id: int) -> list[Lesson]:

    await get_student_or_404(db=db, student_id=student_id)
    
    query = select(Lesson).where(Lesson.student_id == student_id)

    result = await db.execute(query)

    lessons = result.scalars().all()

    if not lessons:
        raise LessonsForStudentNotFound()

    return lessons

#Получение списка логов занятий для ученика
async def get_lesson_logs_for_student_service(db: AsyncSession, student_id: int) -> list[LessonLog]:

    await get_student_or_404(db=db, student_id=student_id)
    
    query = select(LessonLog).where(LessonLog.student_id == student_id)
    result = await db.execute(query)
    lesson_logs = result.scalars().all()

    if not lesson_logs:
        raise LessonLogForStudentNotFound()

    return lesson_logs

#Получение активных абонементов для ученика
async def get_active_subscription_for_student_service(db: AsyncSession, student_id: int) -> Subscription:

    today_date = today()

    await get_student_or_404(db=db, student_id=student_id)
    
    query = select(Subscription).where(
        Subscription.student_id == student_id,
        Subscription.start_date <= today_date,
        Subscription.end_date >= today_date)
    
    result = await db.execute(query)
    subscription = result.scalars().first()

    if subscription is None:
        raise SubscriptionActiveNotFound()
    
    return subscription

#Получение всех абонементов для ученика
async def get_subscriptions_for_student_service(db: AsyncSession, student_id: int) -> list[Subscription]:

    await get_student_or_404(db=db, student_id=student_id)
    
    query = select(Subscription).where(Subscription.student_id == student_id)
    result = await db.execute(query)
    subscriptions = result.scalars().all()

    if not subscriptions:
        raise SubscriptionsForStudentNotFound()

    return subscriptions


#Создание
#Создание ученика
async def create_student_service(db: AsyncSession, data: StudentCreate) -> Student:

    query = (
        select(Student)
        .where(
            Student.first_name == data.first_name,
            Student.last_name == data.last_name,
        )
    )

    if data.phone is not None:
        query = query.where(Student.phone == data.phone)

    result = await db.execute(query)

    existing = result.scalars().first()

    if existing:
        raise StudentAlreadyExists()

    student = Student(**data.model_dump())

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student

#Обновление
#Обновление записи ученика
async def update_student_service(db: AsyncSession, 
                           student_id: int, 
                           data: StudentUpdate,
                           ) -> Student | None:
    
    student = await get_student_or_404(db=db, student_id=student_id)
    
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return student


#Удаление
#Удаление записи ученика
async def delete_student_service(db: AsyncSession, student_id: int) -> Student | None:
    student = await get_student_or_404(db=db, student_id=student_id)
    
    await db.delete(student)
    await db.commit()

    return