from typing import List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation

from app.core.logger import get_logger

logger = get_logger(__name__)


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
        logger.info("Fetched %s users", len(users),)
        return list(users)

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        user = await UserValidation.validate_user(
            user_id=user_id,
            session=self.session,
        )
        await self.session.delete(user)
        await self.session.commit()
