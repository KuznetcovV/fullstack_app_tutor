from pydantic import BaseModel
from datetime import date

class LessonLogCreate(BaseModel):
    student_id: int
    lesson_id: int | None = None
    lesson_log_date: date
    topic: str | None = None
    textbook: str | None = None
    solved_tasks: str | None = None
    grade: int | None = None
    comment: str | None = None

class LessonLogResponse(BaseModel):
    id: int
    student_id: int
    lesson_id: int | None = None
    lesson_log_date: date
    topic: str | None = None
    textbook: str | None = None
    solved_tasks: str | None = None
    grade: int | None = None
    comment: str | None = None

    class Config:
        from_attributes = True

class LessonLogUpdate(BaseModel):
    student_id: int | None = None
    lesson_id: int | None = None
    lesson_log_date: date | None = None
    topic: str | None = None
    textbook: str | None = None
    solved_tasks: str | None = None
    grade: int | None = None
    comment: str | None = None

