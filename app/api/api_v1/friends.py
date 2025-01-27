from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.models.engine import db_helper
from app.core.schemas.friend import GetFriend
from app.core.schemas.user import UserBase
from app.crud.friends import FriendService


router = APIRouter(tags=["friends"])


def get_friend_service(
    user: UserBase = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return FriendService(
        user=user,
        session=session,
    )


@router.get("/friends", response_model=list[GetFriend])
async def get_all_friends(
    friend_service: FriendService = Depends(get_friend_service),
):
    return await friend_service.get_all_friends()


@router.delete("/delete_friendship/{friendship_id}", status_code=204)
async def delete_friendship(
    friend_id: int,
    friend_service: FriendService = Depends(get_friend_service),
):
    return await friend_service.delete_friendship(friend_id=friend_id)
