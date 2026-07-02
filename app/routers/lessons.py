from fastapi import APIRouter

router = APIRouter(prefix="/lessons", tags=["Занятия"])

@router.get("/", summary="Получить все занятия")
def get_lessons():
    return {"message": "lessons list"}