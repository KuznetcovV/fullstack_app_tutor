from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class Student(TimestampMixin, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        unique=True,
        nullable=True
    )

    first_name: Mapped[str] = mapped_column(String(100))

    last_name: Mapped[str] = mapped_column(String(100))

    number_of_class: Mapped[int] = mapped_column()

    phone: Mapped[str | None] = mapped_column()

    parent_name: Mapped[str | None]  = mapped_column()
    parent_phone: Mapped[str | None] = mapped_column()

    notes: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User | None"] = relationship(
        back_populates="student"
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )

    lesson_logs: Mapped[list["LessonLog"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )