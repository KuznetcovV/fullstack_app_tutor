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