from typing import Union
from fastapi import APIRouter, Depends

from app.core.schemas.follower import FollowerSchema, GetFan, GetFollower
from app.core.schemas.friend import FriendSchema, GetFriend
from app.crud.relatonship import RelationshipService
from app.factories.relationship import get_relationship_service


router = APIRouter(tags=["relationship"])


@router.get(
    "/get_all_followers",
    response_model=list[GetFollower],
)
async def get_all_folowers(
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.get_all_folowers()


@router.get(
    "/get_all_fans",
    response_model=list[GetFan],
)
async def get_all_fans(
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.get_all_fans()


@router.post(
    "/following/{follower_id}",
    response_model=Union[FollowerSchema, FriendSchema],
    status_code=201,
)
async def create_follow(
    follower_id: int,
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.create_follow_friendship(follower_id)


@router.delete(
    "/delete_follower/{follower_id}",
    status_code=204,
)
async def delete_follow(
    follower_id: int,
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.delete_follow(follower_id=follower_id)


@router.delete(
    "/delete_fan/{fan_id}",
    status_code=204,
)
async def delete_fan(
    fan_id: int,
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.delete_fan(fan_id=fan_id)


@router.get(
    "/friends",
    response_model=list[GetFriend],
)
async def get_all_friends(
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.get_all_friends()


@router.delete(
    "/delete_friendship/{friendship_id}",
    status_code=204,
)
async def delete_friendship(
    friend_id: int,
    relationship_service: RelationshipService = Depends(
        get_relationship_service
    ),
):
    return await relationship_service.delete_friendship(friend_id=friend_id)
