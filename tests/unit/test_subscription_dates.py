from datetime import date

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

