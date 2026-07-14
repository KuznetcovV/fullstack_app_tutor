from fastapi import APIRouter, Depends, Response, status, HTTPException
from app.services.subscription import create_subscription_service, delete_subscription_service, get_subscriptions_service, get_subscription_by_id_service, update_subscription_service
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.subscription import SubscriptionResponse, SubscriptionCreate, SubscriptionUpdate
from app.models.subscription import Subscription

router = APIRouter(prefix="/subscriptions", tags=["Абонементы"])

@router.get("/",
            response_model=list[SubscriptionResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить все абонементы")
def get_subscriptions(db: Session = Depends(get_db)) -> list[SubscriptionResponse]:
    return get_subscriptions_service(db=db)

@router.get("/{subscription_id}",
            response_model=SubscriptionResponse,
            status_code=status.HTTP_200_OK,
            summary="Получение абонемента по id")
def get_subscription_by_id(
    subscription_id: int,
    db: Session = Depends(get_db)
    ) -> SubscriptionResponse:
    subscription = get_subscription_by_id_service(
        db=db,
        subscription_id=subscription_id
        )
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Абонемент не найден")
    
    return subscription


@router.post("/",
            response_model=SubscriptionResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создание абонемента")
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)) -> SubscriptionResponse:
    return create_subscription_service(db=db, subscription=subscription)


@router.patch("/{subscription_id}",
              response_model=SubscriptionResponse,
              status_code=status.HTTP_200_OK,
              summary="Обновление данных абонемента")
def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    db: Session = Depends(get_db)
    ) -> SubscriptionResponse:
    subscription = update_subscription_service(
        db=db,
        subscription_id=subscription_id,
        data=data)
    
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Абонемент не найден")
    
    return subscription

@router.delete("/{subscription_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление абонемента")
def remove_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
    ):
    subscription = delete_subscription_service(
        subscription_id=subscription_id,
        db=db
        )
    
    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Абонемент не найден")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)