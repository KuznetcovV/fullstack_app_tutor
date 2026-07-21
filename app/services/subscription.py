from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from app.models.subscription import Subscription
from app.models.student import Student
from app.models.lesson import Lesson
from fastapi import HTTPException, status
from sqlalchemy import or_
from datetime import date, timedelta

from app.dependencies.database import get_db



#Получение
async def get_subscriptions_service(
        is_active: bool | None,
        is_paid: bool | None,
        db: AsyncSession
        ) -> list[Subscription]:
    today = date.today()
    query = select(Subscription)
    if is_active == True:
        query = query.where(
            Subscription.start_date <= today,
            Subscription.end_date >= today
            )
        # subscriptions = subscriptions.filter(
        #     Subscription.start_date <= today,
        #     Subscription.end_date >= today
        # )
    elif is_active == False:
        query = query.where(
            or_(
                Subscription.start_date > today,
                Subscription.end_date < today
            ))

    if is_paid is not None:
        query = query.where(
            Subscription.is_paid == is_paid
        )
    
    result = await db.execute(query)
    subscriptions = result.scalars().all()

    return subscriptions

async def get_subscription_by_id_service(db: AsyncSession, subscription_id: int) -> Subscription | None:
    return await db.get(Subscription, subscription_id)


#Создание
async def create_subscription_service(
    db: AsyncSession,
    subscription: SubscriptionCreate
) -> Subscription:

    student = await db.get(Student, subscription.student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден"
        )
    
    await check_existing_lessons_for_subscription(db=db, student_id=student.id)
    await check_intersection_for_existing_subscriptions(db=db, subscription=subscription)

    planned_lessons, total_subscription_price = await calculate_subscription(
        db=db,
        student_id=student.id,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        price_for_one_lesson=subscription.price_for_one_lesson
        )

    subscription_data = subscription.model_dump()

    subscription_data["planned_lessons"] = planned_lessons
    subscription_data["total_price"] = total_subscription_price

    db_subscription = Subscription(**subscription_data)

    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)

    return db_subscription


#Обновление
async def update_subscription_service(db: AsyncSession,
                                subscription_id: int,
                                data: SubscriptionUpdate
                                ) -> Subscription | None:
    subscription = await db.get(Subscription, subscription_id)

    if subscription is None:
        return None
    
    if data.student_id is not None:
        student = await db.get(Student, data.student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ученик не найден")
    

    
    updated_data = data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(subscription, field, value)

    await check_intersection_for_existing_subscriptions(db=db, subscription=subscription, exclude_id=subscription.id)

    need_recalculate = any(
        field in updated_data
        for field in (
            "student_id",
            "start_date",
            "end_date",
            "price_for_one_lesson"
        )
    )

    if need_recalculate:
        planned_lessons, total_price = await calculate_subscription(
            db=db,
            student_id=subscription.student_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            price_for_one_lesson=subscription.price_for_one_lesson
        )

        subscription.planned_lessons = planned_lessons
        subscription.total_price = total_price

    await db.commit()
    await db.refresh(subscription)

    return subscription


#Удаление
async def delete_subscription_service(
        subscription_id: int,
        db: AsyncSession) -> Subscription | None:
    subscription = await db.get(Subscription, subscription_id)
    if subscription is None:
        return None
    
    db.delete(subscription)
    await db.commit()

    return subscription

#вспомогательные функции
async def calculate_subscription(
        db: AsyncSession,
        student_id: int,
        start_date: date,
        end_date: date,
        price_for_one_lesson: Decimal
) -> tuple[int, Decimal]:
    query = select(Lesson).where(Lesson.student_id == student_id)
    result = await db.execute(query)
    lessons = result.scalars().all()
    # lessons = (
    #     db.query(Lesson)
    #     .filter(Lesson.student_id == student_id)
    #     .all()
    # )

    lessons_per_weekday: dict[int, int] = {}

    #кол-во занятий на каждый день недели
    for lesson in lessons:
        lessons_per_weekday[lesson.day] = (
            lessons_per_weekday.get(lesson.day, 0) + 1
        )

    current_date = start_date
    count_lessons = 0

    #проходим по всем датам абонемента
    while current_date <= end_date:
        weekday = current_date.weekday()

        count_lessons += lessons_per_weekday.get(weekday, 0)

        current_date += timedelta(days=1)

    total_price = count_lessons * price_for_one_lesson


    return count_lessons, total_price


async def check_existing_lessons_for_subscription(db: AsyncSession, student_id: int):
    query = select(Lesson).where(Lesson.student_id == student_id)
    result = await db.execute(query)
    lesson_exists = result.scalars().first()
    #lesson_exists = db.query(Lesson).filter(Lesson.student_id == student_id).first()
    if lesson_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Для создания абонемента у ученика должны быть занятия в расписании")
    
async def check_intersection_for_existing_subscriptions(db: AsyncSession, subscription: SubscriptionCreate | Subscription, exclude_id: int | None = None):
    # query = db.query(Subscription).filter(
    #     Subscription.student_id == subscription.student_id
    # )
    query = select(Subscription).where(Subscription.student_id == subscription.student_id)

    if exclude_id is not None:
        query = query.where(Subscription.id != exclude_id)
    
    result = await db.execute(query)
    existing_subscriptions = result.scalars().all()
    # existing_subscriptions = query.all()
    
    for existing in existing_subscriptions:
        if subscription.start_date <= existing.end_date and subscription.end_date >= existing.start_date:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пересечение дат с существующим абонементом для этого ученика")