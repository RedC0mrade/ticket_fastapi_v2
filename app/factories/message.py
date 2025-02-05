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


def get_messages_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
):
    from app.factories.ticket import get_ticket_validation
    from app.validators.ticket import TicketValidation


    valid_ticket: TicketValidation = get_ticket_validation(
        session,
        user,
    )
    valid_message: MessageValidate = get_message_validation(
        session,
        user,
    )

    from app.crud.messages import MessageService

    return MessageService(
        session=session,
        user=user,
        valid_message=valid_message,
        valid_ticket=valid_ticket,
    )
