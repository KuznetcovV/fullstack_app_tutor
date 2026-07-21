from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.lesson_log import LessonLog
from app.models.subscription import Subscription
from app.schemas.student import StudentCreate, StudentUpdate
from sqlalchemy import func, or_
from fastapi import HTTPException, status
from datetime import date

#Получение

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


async def search_students_service(db: AsyncSession, query: str) -> list[Student]:
    query = select(Student).where(or_(Student.first_name.ilike(f"%{query}%"),
                Student.last_name.ilike(f"%{query}%"),
                func.concat(
                    Student.first_name, " ", Student.last_name
                ).ilike(f"%{query}%")))
    
    result = await db.execute(query)
    return result.scalars().all()
    
    # return (
    #     db.query(Student).filter(
    #         or_(
    #             Student.first_name.ilike(f"%{query}%"),
    #             Student.last_name.ilike(f"%{query}%"),
    #             func.concat(
    #                 Student.first_name, " ", Student.last_name
    #             ).ilike(f"%{query}%")
    #         )
    #     ).all()
    # )
    

async def get_student_by_id_service(db: AsyncSession, student_id: int) -> Student | None:
    return await db.get(Student, student_id)

async def get_lessons_for_student_service(db: AsyncSession, student_id: int) -> list[Lesson]:
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    query = select(Lesson).where(Lesson.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_lesson_logs_for_student_service(db: AsyncSession, student_id: int) -> list[LessonLog]:
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    query = select(LessonLog).where(LessonLog.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_active_subscription_for_student_service(db: AsyncSession, student_id: int) -> Subscription:
    today = date.today()
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    query = select(Subscription).where(
        Subscription.student_id == student_id,
        Subscription.start_date <= today,
        Subscription.end_date >= today)
    
    result = await db.execute(query)
    subscription = result.scalars().first()

    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Активных абонементов нет")
    return subscription

async def get_subscriptions_for_student_service(db: AsyncSession, student_id: int) -> list[Subscription]:
    student = await db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    query = select(Subscription).where(Subscription.student_id == student_id)
    result = await db.execute(query)
    return result.scalars().all()


#Создание

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

    student = Student(**data.model_dump())

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой ученик уже существует"
        )

    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

#Обновление

async def update_student_service(db: AsyncSession, 
                           student_id: int, 
                           data: StudentUpdate,
                           ) -> Student | None:
    

    student = await db.get(Student, student_id)

    
    if student is None:
        return None
    
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return student


#Удаление

async def delete_student_service(db: AsyncSession, student_id: int) -> Student | None:
    student = await db.get(Student, student_id)

    if student is None:
        return None
    
    db.delete(student)
    await db.commit()

    return student