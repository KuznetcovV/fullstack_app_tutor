from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    number_of_class: int

class StudentResponse(BaseModel):
    id: int
    name: str
    number_of_class: int

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    name: str | None = None
    number_of_class: int | None = None