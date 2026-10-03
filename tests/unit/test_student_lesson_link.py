from unittest.mock import AsyncMock
from types import SimpleNamespace
import pytest
from app.exceptions.lesson import LessonNotFound
from app.exceptions.student import StudentLessonMismatch
from app.services.lesson_log import check_student_lesson_link

async def test_check_student_lesson_link_passes_when_lesson_belongs_to_student():

    fake_lesson = SimpleNamespace(id=1, student_id=1)

    db = AsyncMock()
    db.get.return_value = fake_lesson

    assert await check_student_lesson_link(db, 1, 1) is None

async def test_check_student_lesson_link_raises_when_lesson_not_found():

    fake_lesson = None

    db = AsyncMock()
    db.get.return_value = fake_lesson


    with pytest.raises(LessonNotFound):
        await check_student_lesson_link(db, 1, 1)


async def test_check_student_lesson_link_raises_when_lesson_belongs_to_different_student():

    fake_lesson = SimpleNamespace(id=1, student_id=2)

    db = AsyncMock()
    db.get.return_value = fake_lesson


    with pytest.raises(StudentLessonMismatch):
        await check_student_lesson_link(db, 1, 1)
