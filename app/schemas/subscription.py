from pydantic import BaseModel, model_validator, field_validator, ConfigDict
from datetime import date
from decimal import Decimal
from app.schemas.base_schemas import BaseSchema

class SubscriptionCreate(BaseSchema):
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
        return value

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date >= self.end_date:
            raise ValueError(
                "Дата начала не может совпадать/быть больше с датой окончания абонемента"
            )
        return self


class SubscriptionResponse(BaseModel):
    id: int
    student_id: int
    start_date: date
    end_date: date
    price_for_one_lesson: Decimal
    is_paid: bool
    planned_lessons: int
    total_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )

class SubscriptionUpdate(BaseSchema):
    student_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    price_for_one_lesson: Decimal | None = None
    is_paid: bool | None = None

    @field_validator("price_for_one_lesson")
    @classmethod
    def validate_price_for_lesson(cls, value):

        if value is None:
            return value

        if value < 0:
            raise ValueError(
                "Цена не может быть отрицательной"
            )
        return value

    @model_validator(mode="after")
    def validate_date(self):
        if (
            self.start_date is not None 
            and self.self.end_date is not None
            and self.start_date >= self.end_date
            ):
            raise ValueError(
                "Дата начала должна быть раньше даты окончания"
            )
        return self