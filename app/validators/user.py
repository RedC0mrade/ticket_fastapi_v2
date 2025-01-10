from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel


async def validate_user(
    user_id: int, session: AsyncSession
) -> UserAlchemyModel:

    searched_user: UserAlchemyModel | None = await session.get(
        UserAlchemyModel, user_id
    )

    if not searched_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return searched_user
