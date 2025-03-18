from fastapi import HTTPException, status
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.auth.schemas import UserRead
from app.core.models.message import MessageAlchemyModel
from app.core.models.ticket import TicketAlchemyModel


class MessageValidate:
    def __init__(
        self,
        user: UserRead,
    ):
        self.user = user

    async def validate_message(
        self,
        message_id: int,
        # user: UserRead,
        session: AsyncSession,
    ) -> MessageAlchemyModel:

        stmt = (
            select(MessageAlchemyModel)
            .where(MessageAlchemyModel.id == message_id)
            .options(
                selectinload(MessageAlchemyModel.ticket).selectinload(
                    TicketAlchemyModel.executor
                )
            )
        )
        result: Result = await session.execute(stmt)
        message: MessageAlchemyModel = result.scalar_one_or_none()

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Message with id = {message_id} not found",
            )

        if not message.ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found",
            )

        if message.ticket.executor_id != self.user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {self.user.id} not executor",
            )

        return message
