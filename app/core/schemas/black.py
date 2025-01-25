from pydantic import BaseModel

from app.core.schemas.user import UserBlackFollowFriend


class BlackUser(BaseModel):
    user_id: int
    black_id: int


class BlacklistUser(BaseModel):
    black_user: UserBlackFollowFriend
