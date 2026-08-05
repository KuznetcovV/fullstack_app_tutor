from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student
from app.exceptions.student import (
    StudentNotFound
)

async def get_student_or_404(db: AsyncSession, student_id: int) -> Student:
    student = await db.get(Student, student_id)

    if student is None:
        raise StudentNotFound()

    return student