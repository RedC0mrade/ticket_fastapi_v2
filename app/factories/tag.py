from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.tags import TagService
from app.factories.database import db_helper

# from app.factories.validation_depends.tag import get_tag_validation


def get_tag_service(
    # valid_tag: TagValidation,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return TagService(session=session)  # , valid_tag=valid_tag)
