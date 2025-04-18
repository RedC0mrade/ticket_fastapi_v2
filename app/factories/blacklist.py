from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.crud.black import BlacklistServices
from app.factories.database import db_helper


def get_blacklist_service(
    user: UserRead = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BlacklistServices:
    return BlacklistServices(
        user=user,
        session=session,
    )
