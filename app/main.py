from fastapi import FastAPI
from app.routers.students import router as students_router
from app.routers.lessons import router as lessons_router
from app.routers.subscriptions import router as subscriptions_router
from app.routers.lesson_logs import router as lesson_logs_router

app = FastAPI()

@app.get('/')
def home():
    return {"message": "Максим, ты уволен"}

app.include_router(students_router,
                   prefix="/students",
                   tags=["Students"])
app.include_router(lessons_router,
                   prefix="/lessons",
                   tags=["Lessons"])
app.include_router(subscriptions_router,
                   prefix="/subscriptions",
                   tags=["Subscriptions"])
app.include_router(lesson_logs_router,
                   prefix="/lesson_logs",
                   tags=["Lesson_logs"])