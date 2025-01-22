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

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"User with id = {user_id} "
                f"don't have follower with id ={follower_id}"
            ),
        )
    return follow
