from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.messages import MessageService
from app.crud.tickets import TicketService
from app.factories.message import get_messages_service
from app.factories.tag import get_tag_validation
from app.validators.tag import TagValidation
from app.validators.ticket import TicketValidation
from app.factories.database import db_helper


def get_ticket_validation(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
) -> TicketValidation:
    return TicketValidation(
        session=session,
        user=user,
    )


def get_ticket_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
    message_service: MessageService = Depends(get_messages_service),
    valid_ticket: TicketValidation = Depends(get_ticket_validation),
    valid_tag: TagValidation = Depends(get_tag_validation),
) -> TicketService:
    return TicketService(
        session=session,
        user=user,
        message_service=message_service,
        valid_ticket=valid_ticket,
        valid_tag=valid_tag
    )
