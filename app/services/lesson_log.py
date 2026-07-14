from sqlalchemy.orm import Session
from app.schemas.lesson_log import LessonLogCreate, LessonLogResponse, LessonLogUpdate
from app.models.lesson_log import LessonLog
from app.models.student import Student
from app.models.lesson import Lesson
from fastapi import HTTPException, status

#Получение
def get_lesson_log_service(
        db: Session
) -> list[LessonLog]:
    return db.query(LessonLog).all()


def get_lesson_log_by_id_service(
        db: Session,
        lesson_log_id: int) -> LessonLog | None:
    return db.get(LessonLog, lesson_log_id)

#Создание
def create_lesson_log_service(db: Session, lesson_log: LessonLogCreate) -> LessonLog:
    student = db.get(Student, lesson_log.student_id)

    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")
    
    if lesson_log.lesson_id is not None:
        lesson = db.get(Lesson, lesson_log.lesson_id)
        if lesson is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Занятие не найдено")
    
    db_lesson_log = LessonLog(**lesson_log.model_dump())
    db.add(db_lesson_log)
    db.commit()
    db.refresh(db_lesson_log)

    return db_lesson_log


#Обновление
def update_lesson_log_service(db: Session, lesson_log_id: int, data: LessonLogUpdate) -> LessonLog | None:
    lesson_log = db.get(LessonLog, lesson_log_id)

    if lesson_log is None:
        return None

    if data.student_id is not None:
        if db.get(Student, data.student_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ученик не найден")

    if data.lesson_id is not None:
        if db.get(Lesson, data.lesson_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Занятие не найдено")

    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(lesson_log, key, value)

    db.commit()
    db.refresh(lesson_log)

    return lesson_log



#Удаление

def delete_lesson_log_service(db: Session, lesson_log_id: int) -> LessonLog | None:
    lesson_log = db.get(LessonLog, lesson_log_id)
    if lesson_log is None:
        return None
    
    db.delete(lesson_log)
    db.commit()

    return lesson_log
