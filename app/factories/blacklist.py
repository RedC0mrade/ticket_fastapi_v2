from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.black import BlacklistServices
from app.factories.database import db_helper
from app.validators.blacklist import BlacklistValidation


def get_blacklist_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BlacklistValidation:
    return BlacklistValidation(session=session)


def get_blacklist_service(
    user: UserBase = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_blacklict: BlacklistValidation = Depends(get_blacklist_validation),
) -> BlacklistValidation:
    return BlacklistServices(
        user=user,
        session=session,
        valid_blacklict=valid_blacklict,
    )
