from pydantic import BaseModel

from app.core.schemas.user import UserFollowFriend


class Friend(BaseModel):
    user_id: int
    friend_id: int


class GetFriend(BaseModel):
    id: int
    friend: UserFollowFriend
