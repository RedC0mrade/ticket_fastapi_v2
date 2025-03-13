from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    password: str | bytes
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    password: str | bytes
    email: EmailStr

class UserPatch(BaseModel):
    username: Optional["str"] = None
    password: Optional["str"] = None
    email: Optional["EmailStr"] = None


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

