from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
import pytest
from app.exceptions.subscription import ZeroLessonsForSubscriptionCreate
from app.services.subscription import check_existing_lessons_for_subscription

async def test_check_existing_lessons_for_subscription_passes_when_lessons_exist():
    fake_lessons = [
        SimpleNamespace(
            id = 1
            ),
        SimpleNamespace(
            id = 2
        )
    ]
    
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    assert await check_existing_lessons_for_subscription(db, 1) is None



async def test_check_existing_lessons_for_subscription_raises_when_no_lessons_exist():
    fake_lessons = []
    
    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    with pytest.raises(ZeroLessonsForSubscriptionCreate):
        await check_existing_lessons_for_subscription(db, 1)
