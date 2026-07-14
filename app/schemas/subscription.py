from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class SubscriptionCreate(BaseModel):
    student_id: int
    start_date: date
    end_date: date
    price: Decimal
    is_paid: bool
    planned_lessons: int

class SubscriptionResponse(BaseModel):
    id: int
    student_id: int
    start_date: date
    end_date: date
    price: Decimal
    is_paid: bool
    planned_lessons: int

    class Config:
        from_attributes = True

class SubscriptionUpdate(BaseModel):
    student_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    price: Decimal | None = None
    is_paid: bool | None = None
    planned_lessons: int | None = None