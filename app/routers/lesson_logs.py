from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.services.lesson_log import create_lesson_log_service, delete_lesson_log_service, get_lesson_log_by_id_service, get_lesson_log_service, update_lesson_log_service


from app.schemas.lesson_log import LessonLogCreate, LessonLogResponse, LessonLogUpdate
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/lesson_logs", tags=["Записи о занятиях"], dependencies=[Depends(get_current_user)])

#Получение
@router.get("/",
            response_model=list[LessonLogResponse],
            status_code=status.HTTP_200_OK,
            summary="Получить все записи о занятиях")
async def get_lesson_logs(db: AsyncSession = Depends(get_db)) -> list[LessonLogResponse]:

    return await get_lesson_log_service(db=db)

@router.get("/{lesson_log_id}",
            response_model=LessonLogResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить запись о занятии по id")
async def get_lesson_log_by_id(
    lesson_log_id: int,
    db: AsyncSession = Depends(get_db)
) -> LessonLogResponse | None:
    
    lesson_log = await get_lesson_log_by_id_service(
        db=db,
        lesson_log_id=lesson_log_id
    )
    
    return lesson_log

@router.post("/",
            response_model=LessonLogResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Создание записи о занятии")
async def create_lesson_log(
    lesson_log: LessonLogCreate,
    db: AsyncSession = Depends(get_db)
) -> LessonLogResponse:

    return await create_lesson_log_service(db=db, lesson_log=lesson_log)

@router.patch("/{lesson_log_id}",
              response_model=LessonLogResponse,
              status_code=status.HTTP_200_OK,
              summary="Обновление данных о записи занятия")
async def update_lesson_log(
    lesson_log_id: int,
    data: LessonLogUpdate,
    db: AsyncSession = Depends(get_db)
) -> LessonLogResponse:
    
    lesson_log = await update_lesson_log_service(
        db=db,
        lesson_log_id=lesson_log_id,
        data=data
    )

    
    return lesson_log

@router.delete("/{lesson_log_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление записи о занятии")
async def remove_lesson_log(
    lesson_log_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    await delete_lesson_log_service(
        lesson_log_id=lesson_log_id,
        db=db
        )
