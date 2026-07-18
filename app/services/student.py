from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.lesson_log import LessonLog
from app.models.subscription import Subscription
from app.schemas.student import StudentCreate, StudentUpdate
from sqlalchemy import func, or_
from fastapi import HTTPException, status
from datetime import date

#Получение

def get_students_service(
        db: Session, 
        number_of_class: int | None, 
        is_active: bool | None
        ) -> list[Student]:
    student_query = db.query(Student)

    if number_of_class is not None:
        student_query = student_query.filter(Student.number_of_class == number_of_class)

    if is_active is not None:
        student_query = student_query.filter(Student.is_active == is_active)

    return student_query.all()


def search_students_service(db: Session, query: str) -> list[Student]:
    return (
        db.query(Student).filter(
            or_(
                Student.first_name.ilike(f"%{query}%"),
                Student.last_name.ilike(f"%{query}%"),
                func.concat(
                    Student.first_name, " ", Student.last_name
                ).ilike(f"%{query}%")
            )
        ).all()
    )
    

def get_student_by_id_service(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)

def get_lessons_for_student_service(db: Session, student_id: int) -> list[Lesson]:
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    return db.query(Lesson).filter(Lesson.student_id == student_id).all()

def get_lesson_logs_for_student_service(db: Session, student_id: int) -> list[LessonLog]:
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    return db.query(LessonLog).filter(LessonLog.student_id == student_id).all()

def get_active_subscription_for_student_service(db: Session, student_id: int) -> Subscription:
    today = date.today()
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    subscription = db.query(Subscription).filter(
        Subscription.student_id == student_id,
        Subscription.start_date <= today,
        Subscription.end_date >= today).first()
    
    if subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Активных абонементов нет")
    return subscription

def get_subscriptions_for_student_service(db: Session, student_id: int) -> list[Subscription]:
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    return db.query(Subscription).filter(Subscription.student_id == student_id).all()


#Создание

def create_student_service(db: Session, data: StudentCreate):

    query = (
        db.query(Student)
        .filter(
            Student.first_name == data.first_name,
            Student.last_name == data.last_name,
        )
    )

    if data.phone is not None:
        query = query.filter(Student.phone == data.phone)

    existing = query.first()

    student = Student(**data.model_dump())

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой ученик уже существует"
        )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student

#Обновление

def update_student_service(db: Session, 
                           student_id: int, 
                           data: StudentUpdate,
                           ) -> Student | None:
    

    student = db.query(Student).filter(Student.id == student_id).first()
    
    if student is None:
        return None
    
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


#Удаление

def delete_student_service(db: Session, student_id: int):
    student = db.get(Student, student_id)

    if student:
        db.delete(student)
        db.commit()

    return student