from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

from app.schemas.user import UserResponse

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str | None = None
    student_id: str | None = None
    plan_id: int | None = None
