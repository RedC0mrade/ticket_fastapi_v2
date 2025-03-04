from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.black_list_user import BlackListAlchemyModel


class BlacklistValidation:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def validate_user_not_in_blacklist(
        self,
        black_id: int,
        user_id: int,
    ) -> BlackListAlchemyModel:

        stmt = select(BlackListAlchemyModel).where(
            BlackListAlchemyModel.user_id == black_id,
            BlackListAlchemyModel.black_id == user_id,
        )

        result: Result = await self.session.execute(stmt)
        blacklist_user = result.scalar_one_or_none()
        if blacklist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"id = {user_id} in blacklist",
            )

    async def validate_user_in_blacklist(
        self,
        black_id: int,
        user_id: int,
    ) -> BlackListAlchemyModel:

        stmt = select(BlackListAlchemyModel).where(
            BlackListAlchemyModel.user_id == black_id,
            BlackListAlchemyModel.black_id == user_id,
        )

        result: Result = await self.session.execute(stmt)
        blacklist_user = result.scalar_one_or_none()
        if not blacklist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"id = {user_id} not in blacklist",
            )
        return blacklist_user
