from fastapi import HTTPException, status
from sqlalchemy import Result, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.follower import FollowerAlchemyModel
from app.core.models.friend import FriendAlchemyModel


class RelationshipValidation:

    @staticmethod
    async def validate_follow(
        follower_id: int,
        session: AsyncSession,
        user_id: int,
    ) -> FollowerAlchemyModel:
        """сheck if the user is already follow"""
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

    @staticmethod
    async def validate_follow_fan_to_delete(
        follower_id: int,
        session: AsyncSession,
        user_id: int,
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

    @staticmethod
    async def validate_follow_fan(
        follower_id: int,
        session: AsyncSession,
        user_id: int,
    ):
        stmt = select(FollowerAlchemyModel).where(
            FollowerAlchemyModel.user_id == user_id,
            FollowerAlchemyModel.follower_id == follower_id,
        )
        result: Result = await session.execute(stmt)
        follow_fan = result.scalar_one_or_none()

        if follow_fan:
            return follow_fan

    @staticmethod
    async def validate_friend(
        friend_id: int,
        session: AsyncSession,
        user_id: int,
    ) -> FriendAlchemyModel:
        stmt = select(FriendAlchemyModel).where(
            and_(
                FriendAlchemyModel.friend_id == friend_id,
                FriendAlchemyModel.user_id == user_id,
            )
        )
        result: Result = await session.execute(stmt)
        friend: FriendAlchemyModel = result.scalar_one_or_none()

        if not friend:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"User with id = {user_id} "
                    f"don't have friend with id = {friend_id}"
                ),
            )
        return friend

    @staticmethod
    async def validate_friendship(
        friend_id: int,
        session: AsyncSession,
        user_id: int,
        is_friend: bool = True,
    ):

        stmt = select(FriendAlchemyModel).where(
            or_(
                and_(
                    FriendAlchemyModel.friend_id == friend_id,
                    FriendAlchemyModel.user_id == user_id,
                ),
                and_(
                    FriendAlchemyModel.friend_id == user_id,
                    FriendAlchemyModel.user_id == friend_id,
                ),
            )
        )
        result: Result = await session.execute(stmt)
        friends = result.scalars().all()
        if friends and is_friend:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Users with id's {user_id} ",
                    f"and {friend_id} already friends",
                ),
            )
        elif not friends and is_friend:
            # проверка в create_follow_friendship на есть ли подписка,
            # перед созданием новой
            # raise HTTPException(
            #     status_code=status.HTTP_400_BAD_REQUEST,
            #     detail=(
            #         f"Users with id's {user_id} ",
            #         f"and {friend_id} not a friends",
            #     ),
            # )
            return None

        return friends
