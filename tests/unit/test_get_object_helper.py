from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest

from app.services.helpers.students import get_student_or_404
from app.services.helpers.lessons import get_lesson_or_404
from app.services.helpers.subscriptions import get_subscription_or_404
from app.services.helpers.lesson_log import get_lesson_log_or_404
from app.services.helpers.user import get_user_or_404

from app.exceptions.student import StudentNotFound
from app.exceptions.lesson import LessonNotFound
from app.exceptions.subscription import SubscriptionNotFound
from app.exceptions.lesson_log import LessonLogNotFound
from app.exceptions.user import UserNotFound

#get_student_or_404
async def test_get_student_or_404_returns_student_when_found():

    fake_student = SimpleNamespace(id=1)

    db = AsyncMock()
    db.get.return_value = fake_student

    result = await get_student_or_404(db, 1)
    assert result is fake_student

async def test_get_student_or_404_raises_when_not_found():

    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(StudentNotFound):
        await get_student_or_404(db, 1)

#get_lesson_or_404
async def test_get_lesson_or_404_returns_lesson_when_found():
    fake_lesson = SimpleNamespace(id=1)

    db = AsyncMock()
    db.get.return_value = fake_lesson

    result = await get_lesson_or_404(db, 1)
    assert result is fake_lesson

async def test_get_lesson_or_404_raises_when_not_found():

    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(LessonNotFound):
        await get_lesson_or_404(db, 1)

#get_subscription_or_404
async def test_get_subscription_or_404_returns_subscription_when_found():
    fake_subscription = SimpleNamespace(id=1)

    db = AsyncMock()
    db.get.return_value = fake_subscription

    result = await get_subscription_or_404(db, 1)
    assert result is fake_subscription

async def test_get_subscription_or_404_raises_when_not_found():

    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(SubscriptionNotFound):
        await get_subscription_or_404(db, 1)

#get_lesson_log_or_404
async def test_get_lesson_log_or_404_returns_lesson_log_when_found():
    fake_lesson_log = SimpleNamespace(id=1)

    db = AsyncMock()
    db.get.return_value = fake_lesson_log

    result = await get_lesson_log_or_404(db, 1)
    assert result is fake_lesson_log

async def test_get_lesson_log_or_404_raises_when_not_found():

    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(LessonLogNotFound):
        await get_lesson_log_or_404(db, 1)

#get_user_or_404
async def test_get_user_or_404_returns_user_when_found():
    fake_user = SimpleNamespace(id=1)

    db = AsyncMock()
    db.get.return_value = fake_user

    result = await get_user_or_404(db, 1)
    assert result is fake_user

async def test_get_user_or_404_raises_when_not_found():

    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(UserNotFound):
        await get_user_or_404(db, 1)