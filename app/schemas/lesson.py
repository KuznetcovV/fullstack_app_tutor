from pydantic import BaseModel
from datetime import time

class LessonCreate(BaseModel):
    student_id: int
    day: int
    time_start: time
    time_end: time

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