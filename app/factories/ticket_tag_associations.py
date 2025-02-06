from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.ticket_tag_association import TicketTagAssociationService
from app.factories.database import db_helper
from app.factories.validation_depends.ticket_tag_association import get_association_validation
from app.validators.ticket_tag_association import AssociationValidation


def get_ticket_tags_association_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_asssociation: AssociationValidation = Depends(
        get_association_validation
    ),
    user: UserBase = Depends(current_auth_user)
) -> TicketTagAssociationService:
    return TicketTagAssociationService(
        session=session,
        valid_asssociation=valid_asssociation,
        user=user,
    )
