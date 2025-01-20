from pydantic import BaseModel, ConfigDict


class Follower(BaseModel):
    user_id: int
    follower_id: int

    model_config = ConfigDict(from_attributes=True)
