from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.friend import FriendAlchemyModel
from app.core.schemas.user import UserWithId
from app.validators.follow import validate_follow
from app.validators.friends import validate_friend, validate_friendshipe


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
            FriendAlchemyModel.user_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        friends = result.scalars().all()
        return friends

    async def create_friend_relationship(
        self,
        friend_id: int,
    ) -> FriendAlchemyModel:
        validate_follow(
            follower_id=self.user.id,
            user_id=friend_id,
        )
        validate_friendshipe(
            user_id=self.user.id,
            friend_id=friend_id,
        )
        stmt = FriendAlchemyModel()
        return friend
