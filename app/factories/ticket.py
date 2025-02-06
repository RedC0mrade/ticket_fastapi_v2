from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.messages import MessageService
from app.crud.tickets import TicketService
from app.factories.message import get_messages_service
from app.factories.tag import get_tag_validation
from app.factories.validation_depends.ticket import get_ticket_validation
from app.validators.tag import TagValidation
from app.factories.database import db_helper


def get_ticket_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
    message_service: MessageService = Depends(get_messages_service),
    valid_tag: TagValidation = Depends(get_tag_validation),
) -> TicketService:
    from app.validators.ticket import TicketValidation

    valid_ticket: TicketValidation = get_ticket_validation(
        session,
        user,
    )
    return TicketService(
        session=session,
        user=user,
        message_service=message_service,
        valid_ticket=valid_ticket,
        valid_tag=valid_tag,
    )
