from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.students import router as students_router
from app.routers.lessons import router as lessons_router
from app.routers.subscriptions import router as subscriptions_router
from app.routers.lesson_logs import router as lesson_logs_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.core.config import FRONTEND_URL
from app.core.handlers import app_exception_handler
from app.core.exceptions import AppException


app = FastAPI()

app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL
        ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', summary="Домашняя страница", tags=["Домашняя страница"])
def home():
    return {"message": "Максим, ты уволен"}

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(lessons_router)
app.include_router(subscriptions_router)
app.include_router(lesson_logs_router)