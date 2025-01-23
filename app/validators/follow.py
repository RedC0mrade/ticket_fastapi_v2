from fastapi import HTTPException, status
from sqlalchemy import Result, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from .friends import validate_friendship


def validate_follow_yourself(
    follower_id: int,
    user_id: int,
):
    if follower_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't follow youself",
        )


async def validate_follow(
    follower_id: int,
    user_id: int,
    session: AsyncSession,
) -> FollowerAlchemyModel:

    validate_follow_yourself(
        follower_id=follower_id,
        user_id=user_id,
    )

    await validate_friendship(
        friend_id=follower_id,
        user_id=user_id,
        session=session,
    )

    stmt = select(FollowerAlchemyModel).where(
        and_(
            FollowerAlchemyModel.follower_id == follower_id,
            FollowerAlchemyModel.user_id == user_id,
        )
    )
    result: Result = await session.execute(stmt)
    follow: FollowerAlchemyModel = result.scalar_one_or_none()

    if follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"User with id = {user_id} "
                f"already have follower with id = {follower_id}"
            ),
        )

    stmt = select(FollowerAlchemyModel).where(
        and_(
            FollowerAlchemyModel.user_id == follower_id,
            FollowerAlchemyModel.follower_id == user_id,
        )
    )
    result: Result = await session.execute(stmt)
    fan: FollowerAlchemyModel = result.scalar_one_or_none()

    return fan


async def validate_follower_relationship(
    follower_id: int, user_id: int, session: AsyncSession
):
    validate_follow_yourself(
        follower_id=follower_id,
        user_id=user_id,
    )
    stmt = select(FollowerAlchemyModel).where(
        FollowerAlchemyModel.user_id == user_id,
        FollowerAlchemyModel.follower_id == follower_id,
    )
    result: Result = await session.execute(stmt)
    follow = result.scalar_one_or_none()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"User with id = {user_id} don't have ",
                f"foloower with id = {follower_id}",
            ),
        )
    return follow
