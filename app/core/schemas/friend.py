from pydantic import BaseModel


class Friend(BaseModel):
    user_id: int
    friend_id: int