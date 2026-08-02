from pydantic import BaseModel
from app.schemas.base_schemas import BaseSchema

class LoginRequest(BaseSchema):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseSchema):
    login: str
    email: str | None = None
    password: str

class RefreshRequest(BaseSchema):
    refresh_token: str

class LogoutResponse(BaseModel):
    message: str