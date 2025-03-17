from pydantic import BaseModel, ConfigDict

from app.core.auth.schemas import UserRead


class FollowerSchema(BaseModel):
    user_id: int
    follower_id: int

    model_config = ConfigDict(from_attributes=True)


class GetFollower(FollowerSchema):
    follower: UserRead


class GetFan(FollowerSchema):
    fan: UserRead
