from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.crud.messages import MessageService
from app.factories.database import db_helper
# from app.factories.validation_depends.message import get_message_validation
# from app.factories.validation_depends.ticket import get_ticket_validation
# from app.validators.message import MessageValidate
# from app.validators.ticket import TicketValidation

def get_messages_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
    # valid_ticket: TicketValidation = Depends(get_ticket_validation),
    # valid_message: MessageValidate = Depends(get_message_validation),
):
    return MessageService(
        session=session,
        user=user,
        # valid_message=valid_message,
        # valid_ticket=valid_ticket,
    )
