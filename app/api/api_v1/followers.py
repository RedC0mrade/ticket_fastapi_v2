from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.models.engine import db_helper
from app.core.schemas.follower import Follower
from app.core.schemas.user import UserWithId
from app.crud.followers import FollowerService


router = APIRouter(tags=["followers"])


def get_follow_service(
    user: UserWithId = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return FollowerService(
        user=user,
        session=session,
    )


@router.post("/following/{follower_id}", response_model = Follower)
async def create_follow(
    follower_id: int,
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.create_follow(follower_id)

@router.delete("/delete/{follower_id}", status_code=204)
async def delete_follow(
    follower_id: int,
    follow_service: FollowerService = Depends(get_follow_service),
):
    return await follow_service.delete_follow(follower_id=follower_id)
