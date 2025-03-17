from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.message import MessageAlchemyModel
from app.core.models.ticket import TicketAlchemyModel
from app.validators.message import MessageValidate
from app.validators.ticket import TicketValidation


class MessageService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserRead,
        valid_message: MessageValidate,
        valid_ticket: TicketValidation,
    ):
        self.session = session
        self.user = user
        self.valid_message = valid_message
        self.valid_ticket = valid_ticket

    async def get_messages(
        self,
        ticket_id: int,
    ) -> List[MessageAlchemyModel]:

        ticket: TicketAlchemyModel = await self.valid_ticket.validate_ticket(
            ticket_id=ticket_id,
            user=self.user,
            session=self.session,
        )

        return list(ticket.messages)

    async def delete_message(
        self,
        message_id: int,
    ) -> None:

        message = await self.valid_message(
            message_id=message_id,
            user=self.user,
            session=self.session,
        )

        await self.session.delete(message)
        await self.session.commit()

    async def delete_all_messages(
        self,
        ticket_id: int,
    ) -> TicketAlchemyModel:

        ticket: TicketAlchemyModel = await self.valid_ticket.validate_ticket(
            ticket_id=ticket_id,
            session=self.session,
        )
        if ticket.executor_id != self.user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You can't delete messages {ticket_id} id's",
            )
        ticket.messages.clear()
        await self.session.commit()
        return ticket

    async def add_message(
        self,
        ticket_id: int,
        message: str,
    ) -> MessageAlchemyModel:

        await self.valid_ticket.validate_ticket(
            ticket_id=ticket_id,
            user=self.user,
            session=self.session,
        )

        message = MessageAlchemyModel(
            message=message,
            ticket_id=ticket_id,
        )
        self.session.add(message)
        await self.session.commit()
        return message

    async def update_message(
        self,
        message_id: int,
        message_text: str,
    ):

        message: MessageAlchemyModel = await self.valid_message(
            message_id=message_id,
            user=self.user,
            session=self.session,
        )
        message.message = message_text
        self.session.add(message)
        await self.session.commit()
        return message
