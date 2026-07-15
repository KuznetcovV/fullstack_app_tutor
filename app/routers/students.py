from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from app.schemas.lesson import LessonResponse
from app.schemas.lesson_log import LessonLogResponse
from app.schemas.subscription import SubscriptionResponse
from app.services.student import (
    get_lesson_logs_for_student_service,
    get_lessons_for_student_service,
    get_students_service,
    search_students_service,
    get_student_by_id_service,
    update_student_service,
    create_student_service,
    delete_student_service,
    get_subscriptions_for_student_service,
    get_active_subscription_for_student_service
)




router = APIRouter(prefix="/students", tags=["Ученики"])

@router.get("/", 
            response_model=list[StudentResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить список учеников")
def get_students(
    number_of_class: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
    ) -> list[StudentResponse]:
    return get_students_service(db, number_of_class, is_active)


@router.get("/search",
            response_model=list[StudentResponse],
            status_code=status.HTTP_200_OK,
            summary="Поиск по имени/фамилии/полному имени")
def search_students(
    query: str,
    db: Session = Depends(get_db)
) -> list[StudentResponse]:
    return search_students_service(query=query, db=db)


@router.get("/{student_id}",
            response_model=StudentResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить конкретного ученика")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)) -> StudentResponse:
    student = get_student_by_id_service(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    
    return student

@router.get("/{student_id}/lesson-logs",
            response_model=list[LessonLogResponse],
            status_code=status.HTTP_200_OK,
            summary="Получение всех записей о занятиях ученика")
def get_lesson_logs_for_student(
    student_id: int,
    db: Session = Depends(get_db)
    ) -> list[LessonLogResponse]:
    lesson_logs = get_lesson_logs_for_student_service(db=db, student_id=student_id)
    return lesson_logs

@router.get("/{student_id}/lessons",
            response_model=list[LessonResponse],
            status_code=status.HTTP_200_OK,
            summary="Получение всех занятий ученика")
def get_lessons_for_student(
    student_id: int,
    db: Session = Depends(get_db)
    ) -> list[LessonResponse]:
    lessons = get_lessons_for_student_service(db=db, student_id=student_id)
    return lessons

@router.get("/{student_id}/subscriptions",
            response_model=list[SubscriptionResponse],
            status_code=status.HTTP_200_OK,
            summary="Получение всех абонементов ученика")
def get_subscriptions_for_student(
    student_id: int,
    db: Session = Depends(get_db)
) -> list[SubscriptionResponse]:
    subscriptions = get_subscriptions_for_student_service(
        db=db,
        student_id=student_id
    )
    return subscriptions

@router.get("/{student_id}/current-subscription",
            response_model=SubscriptionResponse,
            status_code=status.HTTP_200_OK,
            summary="Получение активного абонемента для ученика")
def get_active_subscription_for_student(
    student_id: int,
    db: Session = Depends(get_db)
) -> SubscriptionResponse:
    subscription = get_active_subscription_for_student_service(
        student_id=student_id, db=db
    )
    return subscription

@router.post("/", 
            summary="Добавление ученика",
            status_code=status.HTTP_201_CREATED,
            response_model=StudentResponse)
def create_student(data: StudentCreate,
                   db: Session = Depends(get_db)):
    return create_student_service(db=db, data=data)


@router.patch("/{student_id}",
              summary="Обновление данных ученика",
              status_code=status.HTTP_200_OK,
              response_model=StudentResponse)
def update_student(student_id: int,
                   data: StudentUpdate,
                   db: Session = Depends(get_db)
                   ):
    
    student = update_student_service(db, student_id, data)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Ученик не найден"
            )
    
    return student


@router.delete("/{student_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление ученика")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    student = delete_student_service(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Ученик не найден"
            )
    
    return Response(status_code=204)