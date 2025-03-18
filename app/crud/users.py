from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        valid_user: UserValidation,
    ):
        self.session = session
        self.valid_user = valid_user

    async def get_users(self) -> List[UserAlchemyModel]:
        stmt = select(UserAlchemyModel)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        user = await self.session.get(
            UserAlchemyModel,
            user_id,
        )
        await self.session.delete(user)
        await self.session.commit()
