from pydantic import BaseModel

class LoginRequest(BaseModel):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    login: str
    email: str | None = None
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    message: str