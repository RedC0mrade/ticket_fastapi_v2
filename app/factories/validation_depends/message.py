from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.factories.database import db_helper
from app.validators.message import MessageValidate


def get_message_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
):
    return MessageValidate(
        session=session,
        user=user,
    )