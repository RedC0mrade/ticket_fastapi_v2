from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.black_list_user import BlackListAlchemyModel
from app.validators.blacklist import BlacklistValidation
from app.validators.general import validate_actions_with_same_id
from app.validators.relationship import RelationshipValidation


class BlacklistServices:
    def __init__(
        self,
        user: UserRead,
        session: AsyncSession,
        # valid_blacklict: BlacklistValidation,
        # valid_relationship: RelationshipValidation
    ):
        self.user = user
        self.session = session
        # self.valid_blacklict = valid_blacklict
        # self.valid_relationship = valid_relationship

    async def get_all_blacklist_users(self) -> list[BlackListAlchemyModel]:
        stmt = select(BlackListAlchemyModel).where(
            BlackListAlchemyModel.user_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        black_list = result.scalars().all()
        return black_list

    async def add_to_blacklist(
        self,
        black_id: int,
    ):
        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=black_id,
        )
        await BlacklistValidation.validate_user_not_in_blacklist(
            user_id=self.user.id,
            black_id=black_id,
            session=self.session,
        )
        follow = await RelationshipValidation.validate_follow_fan(
            user_id=black_id,
            follower_id=self.user.id,
            session=self.session,
        )
        if follow:
            await self.session.delete(follow)

        friends = await RelationshipValidation.validate_no_friendship(
            user_id=self.user.id,
            friend_id=black_id,
            session=self.session,
        )

        if friends:
            for user in friends:
                await self.session.delete(user)

        blacklist_user = BlackListAlchemyModel(
            user_id=self.user.id,
            black_id=black_id,
        )
        self.session.add(blacklist_user)
        await self.session.commit()
        return blacklist_user

    async def remove_from_blacklist(
        self,
        black_id: int,
    ) -> None:
        validate_actions_with_same_id(
            user_id=self.user.id,
            second_user_id=black_id,
        )
        blaclist_user = await BlacklistValidation.validate_user_in_blacklist(
            user_id=self.user.id,
            black_id=black_id,
            session=self.session,
        )
        await self.session.delete(blaclist_user)
        await self.session.commit()
