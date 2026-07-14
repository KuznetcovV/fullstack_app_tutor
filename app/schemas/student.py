from pydantic import BaseModel

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    number_of_class: int
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool = True

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    number_of_class: int
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    number_of_class: int | None = None
    phone: str | None = None
    parent_name: str | None = None
    parent_phone: str | None = None
    notes: str | None = None
    is_active: bool | None = None