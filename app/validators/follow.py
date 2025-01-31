from fastapi import HTTPException, status
from sqlalchemy import Result, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel


async def validate_follow(
    follower_id: int,
    user_id: int,
    session: AsyncSession,
) -> FollowerAlchemyModel:

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


async def validate_follow_fan_to_delete(
    follower_id: int,
    user_id: int,
    session: AsyncSession,
):
    stmt = select(FollowerAlchemyModel).where(
        FollowerAlchemyModel.user_id == user_id,
        FollowerAlchemyModel.follower_id == follower_id,
    )
    result: Result = await session.execute(stmt)
    follow_fan = result.scalar_one_or_none()

    if not follow_fan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"User with id = {user_id} don't",
                f"relationship with id = {follower_id}",
            ),
        )
    return follow_fan


async def validate_follow_fan(
    follower_id: int,
    user_id: int,
    session: AsyncSession,
):
    stmt = select(FollowerAlchemyModel).where(
        FollowerAlchemyModel.user_id == user_id,
        FollowerAlchemyModel.follower_id == follower_id,
    )
    result: Result = await session.execute(stmt)
    follow_fan = result.scalar_one_or_none()

    if follow_fan:
        return follow_fan
