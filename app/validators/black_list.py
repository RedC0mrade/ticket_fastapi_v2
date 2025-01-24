from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.black_list_user import BlackListAlchemyModel
from app.core.schemas.user import UserWithId


async def validate_user_in_blacklist(
    black_id: int,
    user: UserWithId,
    session: AsyncSession,
) -> BlackListAlchemyModel:
    stmt = select(BlackListAlchemyModel).where(
        BlackListAlchemyModel.user_id == user.id,
        BlackListAlchemyModel.black_user == black_id,
    )
    result: Result = await session.execute(stmt)
    blacklist_user = result.scalar_one_or_none()
    if blacklist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {black_id} alredy in blacklist",
        )

async def validate_user_not_in_blacklist(
    black_id: int,
    user: UserWithId,
    session: AsyncSession,
) -> BlackListAlchemyModel:
    stmt = select(BlackListAlchemyModel).where(
        BlackListAlchemyModel.user_id == user.id,
        BlackListAlchemyModel.black_user == black_id,
    )
    result: Result = await session.execute(stmt)
    blacklist_user = result.scalar_one_or_none()
    if not blacklist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {black_id} not in blacklist",
        )
    return blacklist_user