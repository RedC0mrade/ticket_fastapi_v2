from typing import List
from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.user import UserAlchemyModel
from app.core.schemas.user import UserWithId
from app.validators.follow import validate_follow


class FollowerService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserWithId,
    ):
        self.session = session
        self.user = user

    async def get_all_folowers(self) -> List[FollowerAlchemyModel]:
        stmt = select(FollowerAlchemyModel).where(
            FollowerAlchemyModel.user_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        followers = result.scalars().all()
        return followers

    async def create_follow(
        self,
        folower_id: int,
    ) -> FollowerAlchemyModel:
        follow = FollowerAlchemyModel(
            user_id=self.user.id,
            follower_id=folower_id,
        )
        self.session.add(follow)
        await self.session.commit()
        return follow

    async def delete_follow(
        self,
        follower_id: int,
    ):
        follow = await validate_follow(
            follower_id=follower_id,
            user=self.user,
            session=self.session,
        )
        await self.session.delete(follow)
        await self.session.commit()
