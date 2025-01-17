from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.ticket_tag_association import TicketTagAssociation
from app.core.schemas.user import UserWithId
from app.core.models.engine import db_helper
from app.crud.ticket_tag_association import TicketTagAssociationService


router = APIRouter(tags=["associations"])


def get_ticket_tags_association_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TicketTagAssociationService:
    return TicketTagAssociationService(session=session)


@router.delete("/{association_id}", status_code=204)
async def delete_association(
    association_id: int,
    ticket_tags_association_service: TicketTagAssociationService = Depends(
        get_ticket_tags_association_service,
    ),
):

    try:
        await ticket_tags_association_service.delete_association(
            association_id=association_id,
        )
    except:
        return Response(status_code=404, content="association not found")


@router.post(
    "/{ticket_id}",
    response_model=list[TicketTagAssociation],
)
async def create_associations(
    tags_ids: List[int],
    ticket_id: int,
    user: UserWithId = Depends(current_auth_user),
    ticket_tags_association_service: TicketTagAssociationService = Depends(
        get_ticket_tags_association_service,
    ),
):
    return await ticket_tags_association_service.create_associations(
        tags_ids=tags_ids,
        ticket_id=ticket_id,
        user=user,
    )
