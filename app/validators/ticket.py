from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.ticket import TicketAlchemyModel
from app.core.schemas.user import UserBase


class TicketValidation:
    def __init__(
        self,
        session: AsyncSession,
        user: UserBase,
    ):
        self.session = session
        self.user = user

    async def validate_ticket(
        self,
        ticket_id: int,
    ) -> TicketAlchemyModel:

        ticket: TicketAlchemyModel = await self.session.get(
            TicketAlchemyModel,
            ticket_id,
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ticket whis id = {ticket_id} not found",
            )

        if ticket.executor_id != self.user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Executor with id = {self.user.id} not found in this ticket",
            )

        return ticket
