from pydantic import BaseModel

from app.core.schemas.user import UserBase


class BlackUser(BaseModel):
    user_id: int
    black_id: int


class BlacklistUser(BlackUser):
    black_user: UserBase
