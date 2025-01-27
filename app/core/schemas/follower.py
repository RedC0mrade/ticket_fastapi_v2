from pydantic import BaseModel, ConfigDict

from app.core.schemas.user import UserBase


class FollowerSchema(BaseModel):
    user_id: int
    follower_id: int

    model_config = ConfigDict(from_attributes=True)


class GetFollower(FollowerSchema):
    follower: UserBase


class GetFan(FollowerSchema):
    fan: UserBase
