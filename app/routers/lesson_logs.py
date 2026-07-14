from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.lesson_log import create_lesson_log_service, delete_lesson_log_service, get_lesson_log_by_id_service, get_lesson_log_service, update_lesson_log_service


from app.schemas.lesson_log import LessonLogCreate, LessonLogResponse, LessonLogUpdate


router = APIRouter(prefix="/lesson_logs", tags=["Записи о занятиях"])

@router.get("/",
            response_model=list[LessonLogResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить все записи о занятиях")
def get_lesson_logs(db: Session = Depends(get_db)) -> list[LessonLogResponse]:
    return get_lesson_log_service(db=db)

@router.get("/{lesson_log_id}",
            response_model=LessonLogResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить запись о занятии по id")
def get_lesson_log_by_id(
    lesson_log_id: int,
    db: Session = Depends(get_db)
) -> LessonLogResponse | None:
    lesson_log = get_lesson_log_by_id_service(
        db=db,
        lesson_log_id=lesson_log_id
    )
    if lesson_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о занятии не найдена"
        )
    
    return lesson_log

@router.post("/",
            response_model=LessonLogResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создание записи о занятии")
def create_lesson_log(
    lesson_log: LessonLogCreate,
    db: Session = Depends(get_db)
) -> LessonLogResponse:
    return create_lesson_log_service(db=db, lesson_log=lesson_log)

@router.patch("/{lesson_log_id}",
              response_model=LessonLogResponse,
              status_code=status.HTTP_200_OK,
              summary="Обновление данных о записи занятия")
def update_lesson_log(
    lesson_log_id: int,
    data: LessonLogUpdate,
    db: Session = Depends(get_db)
) -> LessonLogResponse:
    lesson_log = update_lesson_log_service(
        db=db,
        lesson_log_id=lesson_log_id,
        data=data
    )

    if lesson_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о занятии не найдена"
        )
    
    return lesson_log

@router.delete("/{lesson_log_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление записи о занятии")
def remove_lesson_log(
    lesson_log_id: int,
    db: Session = Depends(get_db)
    ):
    lesson_log = delete_lesson_log_service(
        lesson_log_id=lesson_log_id,
        db=db
        )
    
    if lesson_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о занятии не найдена")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)