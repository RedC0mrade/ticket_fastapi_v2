from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.ticket import TicketAlchemyModel


class TicketValidation:
    @staticmethod
    async def validate_ticket(
        ticket_id: int,
        session: AsyncSession,
        user: UserRead,
    ) -> TicketAlchemyModel:
        ticket: TicketAlchemyModel = await session.get(
            TicketAlchemyModel,
            ticket_id,
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"ticket whis id = {ticket_id} not found",
            )

        if ticket.executor_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Executor with id = {user.id} not found in this ticket",
            )

        return ticket
