from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.factories.database import db_helper
from app.validators.message import MessageValidate
from app.factories.validation_depends.ticket import get_ticket_validation
from app.factories.validation_depends.message import get_message_validation
from app.validators.ticket import TicketValidation
from app.crud.messages import MessageService

def get_messages_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
    valid_ticket: TicketValidation = Depends(get_ticket_validation),
    valid_message: MessageValidate = Depends(get_message_validation),
):
    return MessageService(
        session=session,
        user=user,
        valid_message=valid_message,
        valid_ticket=valid_ticket,
    )
