from typing import List
from fastapi import APIRouter, Depends

from app.core.schemas.ticket_tag_association import TicketTagAssociation
from app.crud.ticket_tag_association import TicketTagAssociationService
from app.factories.ticket_tag_associations import (
    get_ticket_tags_association_service,
)


router = APIRouter(tags=["ticket_tag_association"])


@router.delete(
    "/{association_id}",
    status_code=204,
)
async def delete_association(
    association_id: int,
    ticket_tags_association_service: TicketTagAssociationService = Depends(
        get_ticket_tags_association_service,
    ),
):
    return ticket_tags_association_service.delete_association(
        association_id=association_id,
    )


@router.post(
    "/{ticket_id}",
    response_model=list[TicketTagAssociation],
)
async def create_ticket_tag_association(
    tags_ids: List[int],
    ticket_id: int,
    ticket_tags_association_service: TicketTagAssociationService = Depends(
        get_ticket_tags_association_service,
    ),
):
    return await ticket_tags_association_service.create_associations(
        tags_ids=tags_ids,
        ticket_id=ticket_id,
    )
