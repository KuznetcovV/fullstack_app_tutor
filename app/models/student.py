from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class Student(TimestampMixin, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    number_of_class: Mapped[int] = mapped_column()
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="student"
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="student"
    )

    lesson_logs: Mapped[list["LessonLog"]] = relationship(
        back_populates="student"
    )