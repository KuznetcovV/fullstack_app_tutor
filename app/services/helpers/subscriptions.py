from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription
from app.exceptions.subscription import (
    SubscriptionNotFound
)

async def get_subscription_or_404(db: AsyncSession, subscription_id: int) -> Subscription:
    subscription = await db.get(Subscription, subscription_id)

    if subscription is None:
        raise SubscriptionNotFound()

    return subscription