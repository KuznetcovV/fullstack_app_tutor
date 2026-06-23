from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_lesson_logs():
    return {"message": "lesson logs"}