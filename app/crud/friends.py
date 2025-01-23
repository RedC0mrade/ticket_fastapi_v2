from typing import List
from sqlalchemy import Result, delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.friend import FriendAlchemyModel
from app.core.schemas.user import UserWithId


class FriendService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserWithId,
    ):
        self.session = session
        self.user = user

    async def get_all_friends(self) -> List[FriendAlchemyModel]:
        stmt = select(FriendAlchemyModel).where(
            FriendAlchemyModel.user_id == self.user.id,
        )
        result: Result = await self.session.execute(stmt)
        friends = result.scalars().all()
        return friends

    async def create_friend_relationship(
        self,
        friend_id: int,
    ) -> FriendAlchemyModel:

        friendship = FriendAlchemyModel(
            user_id=self.user.id,
            friend_id=friend_id,
        )
        friendship_follower = FriendAlchemyModel(
            friend_id=self.user.id,
            user_id=friend_id,
        )
        self.session.add_all([friendship, friendship_follower])
        await self.session.commit()
        return friendship

    async def delete_friendship(
        self,
        friend_id,
    ) -> None:

        stmt = delete(FriendAlchemyModel).where(
            or_(
                FriendAlchemyModel.user_id == self.user.id,
                FriendAlchemyModel.user_id == friend_id,
            )
        )
        await self.session.execute(stmt)
        follow = FollowerAlchemyModel(
            user_id=friend_id,
            follower_id=self.user.id,
        )
        self.session.add(follow)
        await self.session.commit()
