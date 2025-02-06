from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.factories.database import db_helper
from app.validators.blacklist import BlacklistValidation


def get_blacklist_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BlacklistValidation:
    return BlacklistValidation(session=session)
