from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_teacher_or_admin
from app.dependencies.database import get_db
from app.schemas.schedule import ScheduleResponse
from datetime import date

from app.services.schedule import get_schedule_service

router = APIRouter(prefix="/schedule", tags=["Расписание"], dependencies=[Depends(get_current_teacher_or_admin)])

@router.get("/",
            response_model=list[ScheduleResponse], 
            status_code=status.HTTP_200_OK, 
            summary="Получить расписание по дням")
async def get_schedule_for_date_or_date_interval(
    date_from: date,
    date_to: date | None = None,
    db: AsyncSession = Depends(get_db)
) -> list[ScheduleResponse]:

    return await get_schedule_service(date_from=date_from, date_to=date_to, db=db)