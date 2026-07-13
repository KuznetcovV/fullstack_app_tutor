from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class Student(TimestampMixin, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    first_name: Mapped[str] = mapped_column(String(100))

    last_name: Mapped[str] = mapped_column(String(100))

    number_of_class: Mapped[int] = mapped_column()

    phone: Mapped[str | None] = mapped_column()

    parent_name: Mapped[str | None]  = mapped_column()
    parent_phone: Mapped[str | None] = mapped_column()

    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="student"
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="student"
    )

    lesson_logs: Mapped[list["LessonLog"]] = relationship(
        back_populates="student"
    )