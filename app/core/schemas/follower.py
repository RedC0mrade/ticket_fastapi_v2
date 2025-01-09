from pydantic import BaseModel


class Follower(BaseModel):
    user_id: int
    follower_id: int
