from datetime import date

from pydantic import ConfigDict, BaseModel
from app.schemas.base_schemas import BaseSchema

class CancelledLessonCreate(BaseSchema):
    lesson_id: int
    lesson_date: date

class CancelledLessonResponse(BaseModel):
    id: int
    lesson_id: int
    lesson_date: date

    model_config = ConfigDict(
        from_attributes=True
    )