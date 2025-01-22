from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.models.engine import db_helper
from app.core.schemas.friend import Friend, GetFriend
from app.core.schemas.user import UserWithId
from app.crud.friends import FriendService


router = APIRouter(tags=["friends"])


def get_friend_service(
    user: UserWithId = Depends(current_auth_user),
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


@router.post("/get_friendship/{friend_id}", response_model=Friend)
async def friend_relationship(
    friend_id: int,
    friend_service: FriendService = Depends(get_friend_service),
):
    return await friend_service.create_friend_relationship(friend_id=friend_id)
