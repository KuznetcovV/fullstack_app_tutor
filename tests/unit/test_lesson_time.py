import pytest
from app.exceptions.lesson import InvalidLessonTimeInterval
from app.services.lesson import validate_lesson_time
from app.models.lesson import Lesson
from app.schemas.lesson import LessonUpdate
from datetime import time

def test_validate_lesson_time_with_valid_interval_passes():
    lesson = Lesson(
        time_start = time(12, 00, 00),
        time_end = time(13, 00, 00)
    )

    data = LessonUpdate(
        time_start=time(13, 00, 00),
        time_end=time(14, 00, 00)
    )

    assert validate_lesson_time(lesson, data) is None

def test_validate_lesson_time_uses_existing_end_when_only_start_provided():
    lesson = Lesson(
        time_start = time(12, 00, 00),
        time_end = time(13, 00, 00)
    )

    data = LessonUpdate(
        time_start=time(12, 30, 00),
    )

    assert validate_lesson_time(lesson, data) is None

def test_validate_lesson_time_uses_existing_start_when_only_end_provided():
    lesson = Lesson(
        time_start = time(12, 00, 00),
        time_end = time(13, 00, 00)
    )

    data = LessonUpdate(
        time_end=time(12, 30, 00),
    )

    assert validate_lesson_time(lesson, data) is None

def test_validate_lesson_time_skips_validation_when_nothing_provided():
    lesson = Lesson(
        time_start = time(12, 00, 00),
        time_end = time(13, 00, 00)
    )

    data = LessonUpdate()

    assert validate_lesson_time(lesson, data) is None