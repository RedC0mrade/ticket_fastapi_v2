from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.factories.database import db_helper
from app.validators.tag import TagValidation


def get_tag_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return TagValidation(session=session)
