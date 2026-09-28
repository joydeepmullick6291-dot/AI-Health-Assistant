from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: Literal["doctor", "patient"]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str