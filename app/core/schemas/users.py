from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    password: str | bytes
    email: EmailStr


class UserPatch(BaseModel):
    username: Optional["str"] = None
    password: Optional["str"] = None
    email: Optional["EmailStr"] = None


class UserWithId(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: bytes
