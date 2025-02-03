from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.friend import FriendAlchemyModel
from app.core.schemas.user import UserBase
from app.validators.friends import validate_friend, validate_no_friendship
from app.validators.general import validate_actions_with_same_id


class FriendService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserBase,
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
        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=friend_id,
        )
        friends = await validate_friend(
            friend_id=friend_id,
            user_id=self.user.id,
        )
        # await self.session.execute(stmt)
        # follow = FollowerAlchemyModel(
        #     user_id=friend_id,
        #     follower_id=self.user.id,
        # )
        self.session.add(follow)
        await self.session.commit()
