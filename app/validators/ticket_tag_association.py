from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)


async def validate_assosiation(
    assosiation_id: int,
    session: AsyncSession,
) -> TicketTagAssociationAlchemyModel:
    assosiation = await session.get(
        TicketTagAssociationAlchemyModel,
        assosiation_id,
    )

    if not assosiation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Association {assosiation_id} not found",
        )
    return assosiation
