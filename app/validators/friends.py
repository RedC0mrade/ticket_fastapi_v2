from fastapi import HTTPException, status
from sqlalchemy import Result, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.friend import FriendAlchemyModel


async def validate_friend(
    friend_id: int,
    user_id: int,
    session: AsyncSession,
) -> FriendAlchemyModel:
    stmt = select(FriendAlchemyModel).where(
        and_(
            FriendAlchemyModel.friend_id == friend_id,
            FriendAlchemyModel.user_id == user_id,
        )
    )
    result: Result = await session.execute(stmt)
    friend: FriendAlchemyModel = result.scalar_one_or_none()

    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"User with id = {user_id} "
                f"don't have friend with id = {friend_id}"
            ),
        )
    return friend


async def validate_friendship(
    friend_id: int,
    user_id: int,
    session: AsyncSession,
) -> FriendAlchemyModel:
    stmt = select(FriendAlchemyModel).where(
        or_(
            and_(
                FriendAlchemyModel.friend_id == friend_id,
                FriendAlchemyModel.user_id == user_id,
            ),
            and_(
                FriendAlchemyModel.friend_id == user_id,
                FriendAlchemyModel.user_id == friend_id,
            ),
        )
    )
    result: Result = await session.execute(stmt)
    friend: FriendAlchemyModel = result.scalar_one_or_none()

    if friend:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Users with id's {user_id} ",
                f"and {friend_id} already friends",
            ),
        )
