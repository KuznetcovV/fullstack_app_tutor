from pydantic import BaseModel, model_validator, field_validator
from datetime import time

class LessonCreate(BaseModel):
    student_id: int
    day: int
    time_start: time
    time_end: time

    @field_validator("day")
    @classmethod
    def validate_day(cls, value):
        if not 0 <= value <= 6:
            raise ValueError(
                "День недели должен быть в диапозоне от 0 до 6, где 0 - понедельник, 6 - воскресенье."
            )
        
        return value
        
    @model_validator(mode="after")
    def validate_time(self):
        if self.time_start >= self.time_end:
            raise ValueError("Время начала не может быть больше или равно времени конца занятия.")
        
        return self



class LessonResponse(BaseModel):
    id: int
    student_id: int
    day: int
    time_start: time
    time_end: time

    class Config:
        from_attributes = True

class LessonUpdate(BaseModel):
    student_id: int | None = None
    day: int | None = None
    time_start: time | None = None
    time_end: time | None = None

    @field_validator("day")
    @classmethod
    def validate_day(cls, value):
        if value is None:
            return value

        if not 0 <= value <= 6:
            raise ValueError(
                "День недели должен быть в диапозоне от 0 до 6, где 0 - понедельник, 6 - воскресенье."
            )
        
        return value
        
    @model_validator(mode="after")
    def validate_time(self):
        if (self.time_start is not None
            and self.time_end is not None
            and self.time_start >= self.time_end):
            raise ValueError("Время начала не может быть больше или равно времени конца занятия.")
        
        return self