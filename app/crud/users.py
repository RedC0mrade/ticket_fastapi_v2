from typing import List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel


class UserService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_users(self) -> List[UserAlchemyModel]:

        stmt = select(UserAlchemyModel).where(
            and_(
                UserAlchemyModel.is_superuser.is_(False),
                UserAlchemyModel.is_verified.is_(True),
            )
        )
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
