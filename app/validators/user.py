from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel


class UserValidation:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def validate_user(
        self,
        user_id: int,
    ) -> UserAlchemyModel:

        valid_user: UserAlchemyModel | None = await self.session.get(
            UserAlchemyModel,
            user_id,
        )

        if not valid_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        if not valid_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not verified",
            )
        return valid_user
