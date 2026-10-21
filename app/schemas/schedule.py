from pydantic import BaseModel
from datetime import time, date

class ScheduleResponse(BaseModel):
    lesson_id: int
    student_id: int
    time_start: time
    time_end: time
    lesson_date: date
