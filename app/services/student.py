from sqlalchemy.orm import Session
from app.models.student import Student


def get_all_students_service(db: Session):
    return db.query(Student).all()

def get_student_by_id_service(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student_service(db: Session, name: str, number_of_class: int):
    student = Student(name=name, number_of_class=number_of_class)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def delete_student_by_id_service(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return student