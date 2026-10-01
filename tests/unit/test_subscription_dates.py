from datetime import date
import pytest

from app.exceptions.subscription import InvalidDatesInetvalError
from app.services.subscription import validate_subscription_dates
from app.schemas.subscription import SubscriptionUpdate
from app.models.subscription import Subscription


def test_validate_subscription_dates_with_valid_interval_passes():
    subscription = Subscription(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31),
    )
    data = SubscriptionUpdate(
        end_date=date(2026, 1, 30),
    )
    assert validate_subscription_dates(subscription, data) is None

def test_validate_subscription_dates_raises_error_when_start_after_end():
    subscription = Subscription(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31),
    )

    data = SubscriptionUpdate(
        start_date=date(2026, 2, 1)
    )

    with pytest.raises(InvalidDatesInetvalError):
        validate_subscription_dates(subscription, data)


def test_validate_subscription_dates_uses_existing_start_when_only_end_provided():
    subscription = Subscription(
        start_date=date(2026, 3, 1),
        end_date=date(2026, 3, 20),
    )

    data = SubscriptionUpdate(
        end_date=date(2026, 1, 1)
    )

    with pytest.raises(InvalidDatesInetvalError):
        validate_subscription_dates(subscription, data)

def test_validate_subscription_dates_uses_existing_end_when_only_start_provided():
    subscription = Subscription(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 20),
    )

    data = SubscriptionUpdate(
        start_date=date(2026, 3, 1)
    )

    with pytest.raises(InvalidDatesInetvalError):
        validate_subscription_dates(subscription, data)

def test_validate_subscription_dates_skips_check_when_both_dates_provided():
    subscription = Subscription(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31),
    )
    data = SubscriptionUpdate(
        start_date=date(2026, 1, 2),
        end_date=date(2026, 1, 30),
    )
    assert validate_subscription_dates(subscription, data) is None