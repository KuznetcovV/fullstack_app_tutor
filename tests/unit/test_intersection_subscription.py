from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from datetime import date
from app.exceptions.subscription import SubscriptionDatesIntersection
from app.models.subscription import Subscription
import pytest

from app.services.subscription import check_intersection_for_existing_subscriptions

async def test_check_intersection_raises_when_dates_overlap():

    fake_sub = [
        SimpleNamespace(
            start_date=date(2026, 10, 1), 
            end_date=date(2026, 10, 15)), 
        SimpleNamespace(
            start_date=date(2026, 10, 15),
            end_date=date(2026, 10, 31)
        )
    ]

    new_subscription = Subscription(
        student_id = 1,
        start_date = date(2026, 10, 30),
        end_date = date(2026, 11, 13)
    )

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_sub
    db.execute.return_value = mock_result

    with pytest.raises(SubscriptionDatesIntersection):
        await check_intersection_for_existing_subscriptions(db, new_subscription)


async def test_passes_when_dates_dont_overlap():

    fake_sub = [
        SimpleNamespace(
            start_date=date(2026, 10, 1), 
            end_date=date(2026, 10, 15)), 
        SimpleNamespace(
            start_date=date(2026, 10, 15),
            end_date=date(2026, 10, 31)
        )
    ]

    new_subscription = Subscription(
        student_id = 1,
        start_date = date(2026, 11, 1),
        end_date = date(2026, 11, 13)
    )

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_sub
    db.execute.return_value = mock_result

    assert await check_intersection_for_existing_subscriptions(db, new_subscription) is None