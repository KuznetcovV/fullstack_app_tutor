from pydantic import BaseModel
from app.models.user import UserRole

class UserResponse(BaseModel):
    id: int
    login: str
    email: str | None
    role: UserRole

    class Config:
        from_attributes = True