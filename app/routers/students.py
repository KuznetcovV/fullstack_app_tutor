from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student import (
    get_all_students_service,
    get_student_by_id_service,
    create_student_service,
    delete_student_by_id_service
)


router = APIRouter(prefix="/students", tags=["Ученики"])

@router.get("/", 
            response_model=list[StudentResponse],
            summary="Получить всех учеников")
def get_all_students(db: Session = Depends(get_db)) -> list:
    return get_all_students_service(db)


@router.get("/{student_id}",
            response_model=StudentResponse,
            summary="Получить конкретного ученика")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)) -> dict:
    student = get_student_by_id_service(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    
    return student



@router.post("/", summary="Добавление ученика")
def create_student(data: StudentCreate,
                   db: Session = Depends(get_db)):
    return create_student_service(db, data.name, data.number_of_class)

@router.delete("/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    student = delete_student_by_id_service(db, student_id)

    if not student:
        raise HTTPException(404, "Ученик не найден")
    
    return {"ok": True}