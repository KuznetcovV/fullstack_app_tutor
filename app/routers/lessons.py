from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.dependencies.database import get_db
from app.services.lesson import (
    create_lesson_service,
    delete_lesson_service,
    get_lesson_by_id_service,
    get_lessons_service,
    update_lesson_service,
    get_today_lesson_service)

router = APIRouter(prefix="/lessons", tags=["Занятия"])

@router.get("/",
            response_model=list[LessonResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить занятия")
async def get_lessons(
    day: int | None = None,
    db: AsyncSession = Depends(get_db)) -> list[LessonResponse]:
    return await get_lessons_service(day=day, db=db)

@router.get("/today",
            response_model=list[LessonResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить сегодняшние занятия")
async def get_today_lessons(
    db: AsyncSession = Depends(get_db)
) -> list[LessonResponse]:
    return await get_today_lesson_service(db=db)

@router.get("/{lesson_id}",
            response_model=LessonResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить урок по id"
            )
async def get_lesson_by_id(lesson_id:int, db: AsyncSession = Depends(get_db)) -> LessonResponse:
    lesson = await get_lesson_by_id_service(db=db, lesson_id=lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Занятие не найдено")
    
    return lesson

@router.post("/",
            response_model=LessonResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создать занятие")
async def create_lesson(
    lesson: LessonCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_lesson_service(db, lesson)


@router.patch("/{lesson_id}",
              response_model=LessonResponse,
              status_code=status.HTTP_200_OK,
              summary="Обновление данных занятия")
async def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: AsyncSession = Depends(get_db)
):

    lesson = await update_lesson_service(db=db,
                                   lesson_id=lesson_id,
                                   data=data)
    
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Урок не найден")
    
    return lesson

@router.delete("/{lesson_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление занятия")
async def remove_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db)
):
    lesson = await delete_lesson_service(db=db, lesson_id=lesson_id)

    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)