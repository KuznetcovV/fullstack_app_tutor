from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription
from datetime import date
from decimal import Decimal

async def seed_subscriptions(db: AsyncSession):

    result = await db.execute(select(Subscription).limit(1))
    exists = result.scalar_one_or_none()
    if exists:
        print("Subscriptions already exists")
        return

    subscriptions = [

        # Иван
        Subscription(
            student_id=1,
            start_date=date(2025, 9, 1),
            end_date=date(2025, 9, 30),
            price_for_one_lesson=Decimal("1200"),
            planned_lessons=13,
            total_price=Decimal("15600"),
            is_paid=True
        ),

        # Мария
        Subscription(
            student_id=2,
            start_date=date(2025, 9, 1),
            end_date=date(2025, 9, 30),
            price_for_one_lesson=Decimal("1500"),
            planned_lessons=9,
            total_price=Decimal("13500"),
            is_paid=False
        ),

        # Дмитрий
        Subscription(
            student_id=3,
            start_date=date(2025, 9, 1),
            end_date=date(2025, 9, 30),
            price_for_one_lesson=Decimal("1800"),
            planned_lessons=9,
            total_price=Decimal("16200"),
            is_paid=True
        ),

        # Антон
        Subscription(
            student_id=4,
            start_date=date(2025, 9, 2),
            end_date=date(2025, 9, 30),
            price_for_one_lesson=Decimal("1000"),
            planned_lessons=9,
            total_price=Decimal("9000"),
            is_paid=False
        ),

        # Екатерина
        Subscription(
            student_id=5,
            start_date=date(2026, 1, 5),
            end_date=date(2026, 1, 31),
            price_for_one_lesson=Decimal("1400"),
            planned_lessons=9,
            total_price=Decimal("12600"),
            is_paid=True
        ),

        # Максим
        Subscription(
            student_id=6,
            start_date=date(2026, 1, 6),
            end_date=date(2026, 1, 31),
            price_for_one_lesson=Decimal("1700"),
            planned_lessons=8,
            total_price=Decimal("13600"),
            is_paid=True
        ),

        # Алина
        Subscription(
            student_id=7,
            start_date=date(2026, 1, 8),
            end_date=date(2026, 2, 8),
            price_for_one_lesson=Decimal("900"),
            planned_lessons=9,
            total_price=Decimal("8100"),
            is_paid=False
        ),

        # Кирилл
        Subscription(
            student_id=8,
            start_date=date(2026, 1, 7),
            end_date=date(2026, 2, 7),
            price_for_one_lesson=Decimal("1600"),
            planned_lessons=9,
            total_price=Decimal("14400"),
            is_paid=True
        ),
    ]

    db.add_all(subscriptions)
    await db.commit()

    print("Subscriptions seeded")