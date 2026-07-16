from pydantic import BaseModel, field_validator
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

    @field_validator("topic", "textbook", "comment")
    @classmethod
    def validate_text_fields(cls, value):
        if value is None:
            return value
        
        if len(value) > 1000:
            raise ValueError("Длина поля не должна превышать 1000 символов")
        return value
        
    @field_validator("grade")
    @classmethod
    def validate_grade(cls, value):
        if value is None:
            return value
        
        if not 2 <= value <= 5:
            raise ValueError("Значение не может быть меньше 2 или больше 5")
        return value


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

    @field_validator("topic", "textbook", "comment")
    @classmethod
    def validate_text_fields(cls, value):
        if value is None:
            return value
        
        if len(value) > 1000:
            raise ValueError("Длина поля не должна превышать 1000 символов")
        return value
        
    @field_validator("grade")
    @classmethod
    def validate_grade(cls, value):
        if value is None:
            return value
        
        if not 2 <= value <= 5:
            raise ValueError("Значение не может быть меньше 2 или больше 5")
        return value

