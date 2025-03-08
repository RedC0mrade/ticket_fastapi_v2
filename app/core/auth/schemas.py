from typing import Optional
from pydantic import EmailStr
from fastapi_users import schemas
from app.core.models.user import UserRoleEnum


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    user_role: UserRoleEnum
