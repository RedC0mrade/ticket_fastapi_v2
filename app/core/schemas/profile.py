from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Profile(BaseModel):
    name: str
    lastname: str
    birthday: date


class CreateProfile(Profile):
    pass


class UpdateProfile:
    name: Optional["str"] = None
    lastname: Optional["str"] = None
    birthday: Optional["date"] = None


class ProfileWithId(Profile):
    id: int

    model_config = ConfigDict(from_attributes=True)
