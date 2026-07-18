from decimal import Decimal

from sqlalchemy.orm import Session
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.models.subscription import Subscription
from app.models.student import Student
from app.models.lesson import Lesson
from fastapi import Depends, HTTPException, status
from sqlalchemy import or_
from datetime import date, timedelta

from app.dependencies.database import get_db



#Получение
def get_subscriptions_service(
        is_active: bool | None,
        is_paid: bool | None,
        db: Session
        ) -> list[Subscription]:
    today = date.today()
    subscriptions = db.query(Subscription)
    if is_active == True:
        subscriptions = subscriptions.filter(
            Subscription.start_date <= today,
            Subscription.end_date >= today
        )
    elif is_active == False:
        subscriptions = subscriptions.filter(
            or_(
                Subscription.start_date > today,
                Subscription.end_date < today
            ))

    if is_paid == True:
        subscriptions = subscriptions.filter(
            Subscription.is_paid == is_paid
        )
        
    return subscriptions.all()

def get_subscription_by_id_service(db: Session, subscription_id: int) -> Subscription | None:
    return db.get(Subscription, subscription_id)


#Создание
def create_subscription_service(
    db: Session,
    subscription: SubscriptionCreate
) -> Subscription:

    student = db.get(Student, subscription.student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден"
        )
    
    check_existing_lessons_for_subscription(db=db, student_id=student.id)
    check_intersection_for_existing_subscriptions(db=db, subscription=subscription)

    planned_lessons, total_subscription_price = calculate_subscription(
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
    db.commit()
    db.refresh(db_subscription)

    return db_subscription


#Обновление
def update_subscription_service(db: Session,
                                subscription_id: int,
                                data: SubscriptionUpdate
                                ) -> Subscription | None:
    subscription = db.get(Subscription, subscription_id)

    if subscription is None:
        return None
    
    if data.student_id is not None:
        student = db.get(Student, data.student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ученик не найден")
    

    
    updated_data = data.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(subscription, field, value)

    check_intersection_for_existing_subscriptions(db=db, subscription=subscription, exclude_id=subscription.id)

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
        planned_lessons, total_price = calculate_subscription(
            db=db,
            student_id=subscription.student_id,
            start_date=subscription.start_date,
            end_date=subscription.end_date,
            price_for_one_lesson=subscription.price_for_one_lesson
        )

        subscription.planned_lessons = planned_lessons
        subscription.total_price = total_price

    db.commit()
    db.refresh(subscription)

    return subscription


#Удаление
def delete_subscription_service(
        subscription_id: int,
        db: Session) -> Subscription | None:
    subscription = db.get(Subscription, subscription_id)
    if subscription is None:
        return None
    
    db.delete(subscription)
    db.commit()

    return subscription

#вспомогательные функции
def calculate_subscription(
        db: Session,
        student_id: int,
        start_date: date,
        end_date: date,
        price_for_one_lesson: Decimal
) -> tuple[int, Decimal]:
    lessons = (
        db.query(Lesson)
        .filter(Lesson.student_id == student_id)
        .all()
    )

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


def check_existing_lessons_for_subscription(db: Session, student_id: int):
    lesson_exists = db.query(Lesson).filter(Lesson.student_id == student_id).first()
    if lesson_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Для создания абонемента у ученика должны быть занятия в расписании")
    
def check_intersection_for_existing_subscriptions(db: Session, subscription: Subscription, exclude_id: int | None = None):
    query = db.query(Subscription).filter(
        Subscription.student_id == subscription.student_id
    )

    if exclude_id is not None:
        query = query.filter(Subscription.id != exclude_id)
    
    existing_subscriptions = query.all()
    
    for existing in existing_subscriptions:
        if subscription.start_date <= existing.end_date and subscription.end_date >= existing.start_date:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пересечение дат с существующим абонементом для этого ученика")