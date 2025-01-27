from pydantic import BaseModel

from app.core.schemas.user import UserBase


class FriendSchema(BaseModel):
    user_id: int
    friend_id: int


class GetFriend(FriendSchema):
    friend: UserBase
