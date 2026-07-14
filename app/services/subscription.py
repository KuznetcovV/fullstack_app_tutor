from sqlalchemy.orm import Session
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.models.subscription import Subscription
from app.models.student import Student
from fastapi import HTTPException, status

#Получение
def get_subscriptions_service(
        db: Session
        ) -> list[Subscription]:
    return db.query(Subscription).all()

def get_subscription_by_id_service(db: Session, subscription_id: int) -> Subscription | None:
    return db.get(Subscription, subscription_id)


#Создание
def create_subscription_service(db: Session, subscription: SubscriptionCreate) -> Subscription:
    student = db.get(Student, subscription.student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ученик не найден")
    
    db_subscription = Subscription(**subscription.model_dump())
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