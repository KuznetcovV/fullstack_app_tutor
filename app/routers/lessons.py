from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.dependencies.database import get_db
from app.services.lesson import create_lesson_service, delete_lesson_service, get_lesson_by_id_service, get_lessons_service, update_lesson_service

router = APIRouter(prefix="/lessons", tags=["Занятия"])

@router.get("/",
            response_model=list[LessonResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить все занятия")
def get_lessons(db: Session = Depends(get_db)) -> list[LessonResponse]:
    return get_lessons_service(db)


@router.get("/{lesson_id}",
            response_model=LessonResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить урок по id"
            )
def get_lesson_by_id(lesson_id:int, db: Session = Depends(get_db)) -> LessonResponse:
    lesson = get_lesson_by_id_service(db=db, lesson_id=lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Занятие не найдено")
    
    return lesson

@router.post("/",
            response_model=LessonResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создать занятие")
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db)
):
    return create_lesson_service(db, lesson)


@router.patch("/{lesson_id}",
              response_model=LessonResponse,
              status_code=status.HTTP_200_OK,
              summary="Обновление данных занятия")
def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: Session = Depends(get_db)
):

    lesson = update_lesson_service(db=db,
                                   lesson_id=lesson_id,
                                   data=data)
    
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Урок не найден")
    
    return lesson

@router.delete("/{lesson_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление занятия")
def remove_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    lesson = delete_lesson_service(db=db, lesson_id=lesson_id)

    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)