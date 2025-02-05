from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.friend import FriendAlchemyModel
from app.core.schemas.user import UserBase
from app.validators.blacklist import BlacklistValidation

from app.validators.general import validate_actions_with_same_id
from app.validators.relationship import RelationshipValidation
from app.validators.user import UserValidation


class RelationshipService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserBase,
        valid_blacklict: BlacklistValidation,
        valid_relationship: RelationshipValidation,
        valid_user: UserValidation,
    ):
        self.session = session
        self.user = user
        self.valid_blacklict = valid_blacklict
        self.valid_relationship = valid_relationship
        self.valid_user = valid_user

    async def get_all_folowers(
        self,
    ) -> List[FollowerAlchemyModel]:
        stmt = select(FollowerAlchemyModel).where(
            FollowerAlchemyModel.user_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        followers = result.scalars().all()
        return followers

    async def get_all_fans(
        self,
    ) -> List[FollowerAlchemyModel]:
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

        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=follower_id,
        )

        self.valid_user.validate_user(user_id=follower_id)
        
        follow: FollowerAlchemyModel = (
            await self.valid_relationship.validate_follow_fan_to_delete(
                follower_id=follower_id,
                user_id=self.user.id,
                session=self.session,
            )
        )
        await self.session.delete(follow)
        await self.session.commit()

    async def delete_fan(
        self,
        fan_id: int,
    ):
        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=fan_id,
        )

        self.valid_user.validate_user(user_id=fan_id)

        fan: FollowerAlchemyModel = (
            await self.valid_relationship.validate_follow_fan_to_delete(
                follower_id=self.user.id,
                user_id=fan_id,
                session=self.session,
            )
        )
        await self.session.delete(fan)
        await self.session.commit()

    async def create_follow_friendship(
        self,
        follower_id: int,
    ) -> FollowerAlchemyModel | FriendAlchemyModel:

        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=follower_id,
        )

        self.valid_user.validate_user(user_id=follower_id)

        await self.valid_blacklict.validate_user_not_in_blacklist(
            black_id=follower_id,
            user_id=self.user.id,
            session=self.session,
        )
        await self.valid_relationship.validate_follow(
            follower_id=follower_id,
            user_id=self.user.id,
            session=self.session,
        )
        await self.valid_relationship.validate_friendship(
            friend_id=follower_id,
            user_id=self.user.id,
            session=self.session,
        )
        fan: FollowerAlchemyModel = (
            await self.valid_relationship.validate_follow_fan(
                follower_id=self.user.id,
                user_id=follower_id,
                session=self.session,
            )
        )

        if fan:
            friendship = await self.create_friend_relationship(
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

    async def get_all_friends(
        self,
    ) -> List[FriendAlchemyModel]:
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
        friends = await self.valid_relationship.validate_friendship(
            friend_id=friend_id,
            user_id=self.user.id,
            is_friend=False,
        )
        for friend in friends:
            await self.session.delete(friend)
        await self.session.commit()

        await self.create_follow_friendship()
        
        follow = FollowerAlchemyModel(
            follower_id=self.user.id,
            user_id=friend_id,
        )
        
        self.session.add(follow)
        await self.session.commit()
