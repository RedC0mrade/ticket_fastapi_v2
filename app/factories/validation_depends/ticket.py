from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.factories.database import db_helper
from app.validators.ticket import TicketValidation


def get_ticket_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
) -> TicketValidation:

    return TicketValidation(
        session=session,
        user=user,
    )
