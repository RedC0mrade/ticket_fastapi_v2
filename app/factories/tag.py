from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.crud.tags import TagService
from app.factories.database import db_helper
from app.factories.validation_depends.tag import get_tag_validation
from app.validators.tag import TagValidation


def get_tag_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_tag: TagValidation = Depends(get_tag_validation),
):
    return TagService(session=session, valid_tag=valid_tag)
