from fastapi import APIRouter, Depends, status
from app.dependencies.auth import get_current_teacher_or_admin
from app.dependencies.database import get_db
from app.schemas.cancelled_lesson import CancelledLessonCreate, CancelledLessonResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cancelled_lesson import create_cancelled_lesson_service, get_cancelled_lessons_service


router = APIRouter(prefix="/cancelled-lessons", tags=["Записи об отменах занятий"], dependencies=[Depends(get_current_teacher_or_admin)])

@router.post("/",
             response_model=CancelledLessonResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Создание отмены занятия")
async def create_cancelled_lesson(cancelled_lesson: CancelledLessonCreate,
                                  db: AsyncSession = Depends(get_db)) -> CancelledLessonResponse:
    
    return await create_cancelled_lesson_service(db=db, cancelled_lesson=cancelled_lesson)

@router.get("/",
            response_model=list[CancelledLessonResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить все записи об отменах")
async def get_cancelled_lessons(
    db: AsyncSession = Depends(get_db)
) -> list[CancelledLessonResponse]:

    return await get_cancelled_lessons_service(db=db)