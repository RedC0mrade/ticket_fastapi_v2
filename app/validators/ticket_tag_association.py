from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)


class AssociationValidation:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def validate_assosiation(
        self,
        assosiation_id: int,
    ) -> TicketTagAssociationAlchemyModel:
        assosiation = await self.session.get(
            TicketTagAssociationAlchemyModel,
            assosiation_id,
        )

        if not assosiation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Association {assosiation_id} not found",
            )
        return assosiation
