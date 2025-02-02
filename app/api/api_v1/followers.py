from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.friends import get_friend_service
from app.authentication.actions import current_auth_user
from app.factories.database import db_helper
from app.core.schemas.follower import FollowerSchema, GetFan, GetFollower
from app.core.schemas.friend import FriendSchema
from app.core.schemas.user import UserBase
from app.crud.followers import FollowerService
from app.crud.friends import FriendService


router = APIRouter(tags=["followers"])


def get_follow_service(
    user: UserBase = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
    friend_service: FriendService = Depends(get_friend_service),
):
    return FollowerService(
        user=user, session=session, friend_service=friend_service
    )


@router.get("/get_all_followers", response_model=list[GetFollower])
async def get_all_folowers(
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.get_all_folowers()


@router.get("/get_all_fans", response_model=list[GetFan])
async def get_all_fans(
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.get_all_fans()


@router.post(
    "/following/{follower_id}",
    response_model=Union[FollowerSchema, FriendSchema],
    status_code=201,
)
async def create_follow(
    follower_id: int,
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.create_follow_friendship(follower_id)


@router.delete("/delete_follower/{follower_id}", status_code=204)
async def delete_follow(
    follower_id: int,
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.delete_follow(follower_id=follower_id)


@router.delete("/delete_fan/{fan_id}", status_code=204)
async def delete_fan(
    fan_id: int,
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.delete_fan(fan_id=fan_id)
