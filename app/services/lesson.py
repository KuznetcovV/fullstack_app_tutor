from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.models.student import Student
from app.schemas.lesson import LessonCreate, LessonUpdate
from fastapi import HTTPException

#Получение
def get_lessons_service(db: Session) -> list[Lesson]:
    return db.query(Lesson).all()

def get_lesson_by_id_service(db: Session, lesson_id: int) -> Lesson | None:
    return db.get(Lesson, lesson_id)

#Создание
def create_lesson_service(db: Session, lesson: LessonCreate) -> Lesson:
    student = db.get(Student, lesson.student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Ученик не найден")
    
    db_lesson = Lesson(**lesson.model_dump())

    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

    return db_lesson

#Обновление
def update_lesson_service(db: Session,
                          lesson_id: int,
                          data: LessonUpdate
                          ) -> Lesson | None:
    
    lesson = db.get(Lesson, lesson_id)

    if lesson is None:
        return None

    if data.student_id is not None:
        student = db.get(Student, data.student_id)

        if student is None:
            raise HTTPException(status_code=404,
                                detail="Ученик не найден")
    
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)

    return lesson

#Удаление
def delete_lesson_service(db: Session,
                          lesson_id: int) -> Lesson | None:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        return None
    
    db.delete(lesson)
    db.commit()

    return lesson