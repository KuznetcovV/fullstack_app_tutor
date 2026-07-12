from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentUpdate


#Получение

def get_all_students_service(db: Session):
    return db.query(Student).all()

def get_student_by_id_service(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_name_service(db: Session, student_name: str) -> Student | None:
    return db.query(Student).filter(Student.name == student_name).first()


#Создание

def create_student_service(db: Session, name: str, number_of_class: int):
    student = Student(name=name, number_of_class=number_of_class)
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