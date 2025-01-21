from pydantic import BaseModel, ConfigDict

from app.core.schemas.user import UserFollow


class FollowerModelSchema(BaseModel):
    user_id: int
    follower_id: int

    model_config = ConfigDict(from_attributes=True)


class GetFollower(BaseModel):
    follower: UserFollow
