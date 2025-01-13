from fastapi import HTTPException, status
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.models.message import MessageAlchemyModel
from app.core.models.ticket import TicketAlchemyModel
from app.core.schemas.user import UserWithId


async def validate_message(
    message_id: int,
    user: UserWithId,
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

    if message.ticket.executor_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user.id} not executor",
        )

    return message
