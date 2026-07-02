from sqlalchemy import ForeignKey, Date, Numeric, Boolean
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin
from decimal import Decimal

class Subscription(TimestampMixin, Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))

    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    price: Mapped[Decimal] = mapped_column(Numeric(8, 2))

    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)

    planned_lessons: Mapped[int] = mapped_column(default=0)

    student: Mapped["Student"] = relationship(
        back_populates="subscriptions"
    )

    @property
    def is_active(self):
        return self.start_date <= date.today() <= self.end_date
    
    @property
    def full_cost(self):
        return self.planned_lessons * self.price