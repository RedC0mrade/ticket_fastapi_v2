from typing import Optional
from pydantic import EmailStr
from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool
