from sqlalchemy.orm import Session
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.models.subscription import Subscription
from app.models.student import Student
from app.models.lesson import Lesson
from fastapi import HTTPException, status
from sqlalchemy import or_
from datetime import date, timedelta



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
def create_subscription_service(db: Session, subscription: SubscriptionCreate) -> Subscription:
    student = db.get(Student, subscription.student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден")
    
    lesson_weekdays = set([lesson.day for lesson in db.query(Lesson).filter(Lesson.student_id == subscription.student_id).all()])
    current_date = subscription.start_date
    count_lessons = 0
    while current_date <= subscription.end_date:
        weekday = current_date.weekday()
        if weekday in lesson_weekdays:
            count_lessons += 1
        
        current_date += timedelta(days=1)
    
    db_subscription = subscription.model_dump()
    total_price = count_lessons * db_subscription["price_for_one_lesson"]
    db_subscription["planned_lessons"] = count_lessons
    db_subscription["total_price"] = total_price
    db_subscription = Subscription(**db_subscription)
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