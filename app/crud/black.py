from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.black_list_user import BlackListAlchemyModel
from app.core.schemas.user import UserBase
from app.validators.black_list import (
    validate_user_in_blacklist,
    validate_user_not_in_blacklist,
)
from app.validators.friends import validate_no_friendship


class BlacklistServices:
    def __init__(
        self,
        user: UserBase,
        session: AsyncSession,
    ):
        self.user = user
        self.session = session

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
        await validate_user_in_blacklist(
            user_id=self.user.id,
            black_id=black_id,
            session=self.session,
        )
        
        friends = await validate_no_friendship(
            user_id=self.user.id,
            friend_id = black_id,
            session=self.session,
        )
        if friends:
            print(friends)
            
        # blacklist_user = BlackListAlchemyModel(
        #     user_id=self.user.id,
        #     black_id=black_id,
        # )
        # self.session.add(blacklist_user)
        # await self.session.commit()
        # return blacklist_user

    async def remove_from_blacklist(
        self,
        black_id: int,
    ) -> None:
        blaclist_user = await validate_user_not_in_blacklist(
            user_id=self.user.id,
            black_id=black_id,
            session=self.session,
        )
        await self.session.delete(blaclist_user)
        await self.session.commit()
