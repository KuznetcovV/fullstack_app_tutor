from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from datetime import time
import pytest
from app.exceptions.lesson import LessonTimeIntersection
from app.models.lesson import Lesson

from app.services.lesson import check_lessons_intersection



async def test_check_lessons_intersection_raises_when_time_overlaps_same_day():
    fake_lessons = [
        SimpleNamespace(day=0, time_start=time(12, 0, 0), time_end=time(13, 0, 0)),
        SimpleNamespace(day=3, time_start=time(12, 0, 0), time_end=time(13, 0, 0))
        ]

    new_lesson = Lesson(
        day=0, 
        time_start=time(12, 30, 0), 
        time_end=time(13, 30, 0)
        )

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    with pytest.raises(LessonTimeIntersection):
        await check_lessons_intersection(db, new_lesson)

async def test_check_lessons_intersection_passes_when_different_days():
    fake_lessons = []

    new_lesson = Lesson(
        day=1, 
        time_start=time(12, 30, 0), 
        time_end=time(13, 30, 0)
        )

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    assert await check_lessons_intersection(db, new_lesson) is None

async def test_check_lessons_intersection_passes_when_times_dont_overlap():
    fake_lessons = [
        SimpleNamespace(day=0, time_start=time(12, 0, 0), time_end=time(13, 0, 0)),
        ]

    new_lesson = Lesson(
        day=0, 
        time_start=time(13, 30, 0), 
        time_end=time(14, 30, 0)
        )

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    assert await check_lessons_intersection(db, new_lesson) is None