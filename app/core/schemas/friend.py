from pydantic import BaseModel

from app.core.schemas.user import UserBlackFollowFriend


class Friend(BaseModel):
    user_id: int
    friend_id: int


class GetFriend(BaseModel):
    friend: UserBlackFollowFriend
