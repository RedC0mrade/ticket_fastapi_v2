from pydantic import BaseModel

from app.core.auth.schemas import UserRead


class BlackUser(BaseModel):
    user_id: int
    black_id: int


class BlacklistUser(BlackUser):
    black_user: UserRead
