from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation
from app.core.models import db_helper
from app.core.auth.schemas import UserRead
from app.crud.users import UserService
from app.factories.user import get_user_service
from app.api.dependencies.current_users_depends import current_active_user
router = APIRouter(tags=["test"])


@router.get(
    "/all_users",
    response_model=list[UserRead],
)
async def get_users(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user)
) -> List[UserAlchemyModel]:

    stmt = select(UserAlchemyModel).where(
        and_(
            UserAlchemyModel.is_superuser.is_(False),
            UserAlchemyModel.is_verified.is_(True),
        )
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)
