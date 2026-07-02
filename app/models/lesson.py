from sqlalchemy import ForeignKey, Time, Date, UniqueConstraint
from datetime import time, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class Lesson(TimestampMixin, Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )

    day: Mapped[int] = mapped_column()

    time_start: Mapped[time] = mapped_column(Time)
    time_end: Mapped[time] = mapped_column(Time)
    student: Mapped["Student"] = relationship(
        back_populates="lessons"
    )

    cancelled_lessons: Mapped[list["CancelledLesson"]] = relationship(
        back_populates="lesson"
    )

    transferred_lessons: Mapped[list["TransferredLesson"]] = relationship(
        back_populates="lesson"
    )

    lesson_logs: Mapped[list["LessonLog"]] = relationship(
        back_populates="lesson"
    )



class CancelledLesson(TimestampMixin, Base):
    __tablename__ = "cancelled_lessons"

    __table_args__ = (
        UniqueConstraint(
            "lesson_id",
            "lesson_date",
            name="uq_cancelled_lesson_date",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    lesson_date: Mapped[date] = mapped_column(Date)

    lesson: Mapped["Lesson"] = relationship(
        back_populates="cancelled_lessons"
    )


class TransferredLesson(TimestampMixin, Base):
    __tablename__ = "transferred_lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    old_date: Mapped[date] = mapped_column(Date)
    new_date: Mapped[date] = mapped_column(Date)

    new_time_start: Mapped[time] = mapped_column(Time)
    new_time_end: Mapped[time] = mapped_column(Time)

    lesson: Mapped["Lesson"] = relationship(
        back_populates="transferred_lessons"
    )
 