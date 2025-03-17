from pydantic import BaseModel

from app.core.auth.schemas import UserRead


class FriendSchema(BaseModel):
    user_id: int
    friend_id: int


class GetFriend(FriendSchema):
    friend: UserRead
