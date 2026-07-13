from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from sqlalchemy import func, or_


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
    return db.query(Student).filter(Student.id == student_id).first()


#Создание

def create_student_service(db: Session, data: StudentCreate):

    student = Student(**data.model_dump())

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

def delete_student_by_id_service(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return student