from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase

from app.factories.database import db_helper
from app.validators.ticket import TicketValidation



def get_ticket_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
) -> TicketValidation:

    return TicketValidation(
        session=session,
        user=user,
    )