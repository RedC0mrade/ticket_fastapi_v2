from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.friend import FriendAlchemyModel
from app.core.schemas.user import UserBase
from app.crud.friends import FriendService
from app.validators.follow import (
    validate_follow,
    validate_follower_relationship,
)


class FollowerService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserBase,
        friend_service: FriendService,
    ):
        self.session = session
        self.user = user
        self.friend_service = friend_service

    async def get_all_folowers(self) -> List[FollowerAlchemyModel]:
        stmt = select(FollowerAlchemyModel).where(
            FollowerAlchemyModel.user_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        followers = result.scalars().all()
        return followers

    async def get_all_fans(self) -> List[FollowerAlchemyModel]:
        stmt = select(FollowerAlchemyModel).where(
            FollowerAlchemyModel.follower_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        fans = result.scalars().all()
        return fans

    async def delete_follow(
        self,
        follower_id: int,
    ):
        follow = await validate_follower_relationship(
            follower_id=follower_id,
            user_id=self.user.id,
            session=self.session,
        )
        await self.session.delete(follow)
        await self.session.commit()

    async def delete_fan(
        self,
        fan_id: int,
    ):
        fan = await validate_follower_relationship(
            follower_id=self.user.id,
            user_id=fan_id,
            session=self.session,
        )
        await self.session.delete(fan)
        await self.session.commit()

    async def create_follow_friendship(
        self,
        follower_id: int,
    ) -> FollowerAlchemyModel | FriendAlchemyModel:

        fan: FollowerAlchemyModel = await validate_follow(
            follower_id=follower_id,
            user_id=self.user.id,
            session=self.session,
        )

        if fan:
            friendship = await self.friend_service.create_friend_relationship(
                friend_id=follower_id,
            )
            await self.session.delete(fan)
            await self.session.commit()
            return friendship

        follow = FollowerAlchemyModel(
            follower_id=follower_id,
            user_id=self.user.id,
        )

        self.session.add(follow)
        await self.session.commit()
        return follow
