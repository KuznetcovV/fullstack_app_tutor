from sqlalchemy import ForeignKey, Date, Text, String
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.mixins import TimestampMixin

class LessonLog(TimestampMixin, Base):
    __tablename__ = "lesson_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
        )

    lesson_id: Mapped[int| None] = mapped_column(
        ForeignKey("lessons.id", ondelete="SET NULL"), 
        nullable=True
        )
    
    lesson_log_date: Mapped[date] = mapped_column(Date)

    topic: Mapped[str | None] = mapped_column(Text, nullable=True)

    textbook: Mapped[str| None] = mapped_column(String(255), nullable=True)

    solved_tasks: Mapped[str| None] = mapped_column(Text, nullable=True)

    grade: Mapped[int| None] = mapped_column(nullable=True)

    comment: Mapped[str| None] = mapped_column(Text, nullable=True)

    student: Mapped["Student"] = relationship(
        back_populates="lesson_logs"
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="lesson_logs"
    )