from typing import List
from fastapi import HTTPException
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)
from app.core.models.ticket import TicketAlchemyModel
from app.validators.tag import TagValidation
from app.validators.ticket import TicketValidation
from app.validators.ticket_tag_association import AssociationValidation


class TicketTagAssociationService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserRead,
        # valid_asssociation: AssociationValidation,
        # valid_tag: TagValidation,
        # valid_ticket: TicketValidation,
    ):
        self.session = session
        self.user = user
        # self.valid_asssociation = valid_asssociation
        # self.valid_tag = valid_tag
        # self.valid_ticket = valid_ticket

    async def create_associations(
        self,
        tags_ids: List[int],
        ticket_id: int,
    ) -> List[TicketTagAssociationAlchemyModel]:
        ticket: TicketAlchemyModel = await TicketValidation.validate_ticket(
            ticket_id=ticket_id,
            user=self.user,
            session=self.session,
        )
        await TagValidation.validate_tags_in_base(
            tags=tags_ids,
            session=self.session,
        )
        if ticket.tags:
            await self.delete_all_associatons_in_ticket(
                ticket_id=ticket_id,
                session=self.session,
            )
        association_data = [
            {"tag_id": tag_id, "ticket_id": ticket_id} for tag_id in tags_ids
        ]
        stmt = insert(TicketTagAssociationAlchemyModel).values(
            association_data,
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return association_data

    async def delete_association(
        self,
        association_id: int,
    ) -> None:
        association: TicketTagAssociationAlchemyModel = (
            await AssociationValidation.validate_assosiation(
                assosiation_id=association_id,
                session=self.session,
            )
        )
        await self.session.delete(association)
        await self.session.commit()

    async def delete_all_associatons_in_ticket(
        self,
        ticket_id: int,
    ) -> None:
        stmt = delete(TicketTagAssociationAlchemyModel).where(
            TicketTagAssociationAlchemyModel.ticket_id == ticket_id
        )
        result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No associations found for ticket_id {ticket_id}",
            )
