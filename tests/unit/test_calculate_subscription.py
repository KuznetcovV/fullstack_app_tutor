from unittest.mock import AsyncMock, MagicMock
from types import SimpleNamespace
from datetime import date
from app.services.subscription import calculate_subscription
from decimal import Decimal

async def test_calculate_subscription_counts_lessons_for_single_weekday():
    fake_lessons = [SimpleNamespace(day=0), SimpleNamespace(day=0)]

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    start_date = date(2026, 10, 1)
    end_date = date(2026, 10, 31)

    count, price = await calculate_subscription(db=db, 
                                          student_id=1, 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          price_for_one_lesson=Decimal("1000.00"))

    assert count == 8
    assert price == Decimal("8000.00")

async def test_calculate_subscription_counts_lessons_for_multiple_weekdays():
    fake_lessons = [SimpleNamespace(day=0), SimpleNamespace(day=2), SimpleNamespace(day=1)]

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    start_date = date(2026, 10, 1)
    end_date = date(2026, 10, 31)

    count, price = await calculate_subscription(db=db, 
                                          student_id=1, 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          price_for_one_lesson=Decimal("1000.00"))

    assert count == 12
    assert price == Decimal("12000.00")

async def test_calculate_subscription_returns_zero_when_no_lessons_in_period():
    fake_lessons = []

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    start_date = date(2026, 10, 1)
    end_date = date(2026, 10, 31)

    count, price = await calculate_subscription(db=db, 
                                          student_id=1, 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          price_for_one_lesson=Decimal("1000.00"))

    assert count == 0
    assert price == Decimal("0.00")

async def test_calculate_subscription_multiplies_price_correctly():
    fake_lessons = [SimpleNamespace(day=1), SimpleNamespace(day=1)]

    db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_lessons
    db.execute.return_value = mock_result

    start_date = date(2026, 10, 5)
    end_date = date(2026, 10, 11)

    count, price = await calculate_subscription(db=db, 
                                          student_id=1, 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          price_for_one_lesson=Decimal("1234.56"))

    assert count == 2
    assert price == Decimal("2469.12")
