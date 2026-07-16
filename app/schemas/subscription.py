from pydantic import BaseModel, model_validator, field_validator
from datetime import date
from decimal import Decimal

class SubscriptionCreate(BaseModel):
    student_id: int
    start_date: date
    end_date: date
    price_for_one_lesson: Decimal
    is_paid: bool

    @field_validator("price_for_one_lesson")
    @classmethod
    def validate_price_for_lesson(cls, value):
        if value < 0:
            raise ValueError(
                "Цена не может быть отрицательной"
            )

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date <= self.end_date:
            raise ValueError(
                "Дата начала не может совпадать/быть больше с датой окончания абонемента"
            )


class SubscriptionResponse(BaseModel):
    id: int
    student_id: int
    start_date: date
    end_date: date
    price_for_one_lesson: Decimal
    is_paid: bool
    planned_lessons: int
    total_price: Decimal

    class Config:
        from_attributes = True

class SubscriptionUpdate(BaseModel):
    student_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    price_for_one_lesson: Decimal | None = None
    is_paid: bool | None = None
    planned_lessons: int | None = None
    total_price: Decimal | None = None

    @field_validator("price_for_one_lesson")
    @classmethod
    def validate_price_for_lesson(cls, value):
        if value < 0:
            raise ValueError(
                "Цена не может быть отрицательной"
            )
        
    @field_validator("planned_lessons")
    @classmethod
    def validate_planned_lessons(cls, value):
        if value <= 0:
            raise ValueError(
                "Кол-во занятий должно быть положительным числом"
            )
    
    @field_validator("total_price")
    @classmethod
    def validate_total_price(cls, value):
        if value < 0:
            raise ValueError(
                "Стоимость абонемента не может быть отрицательной"
            )


    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date <= self.end_date:
            raise ValueError(
                "Дата начала не может совпадать/быть больше с датой окончания абонемента"
            )