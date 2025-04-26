from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.crud.ticket_tag_association import TicketTagAssociationService
from app.factories.database import db_helper

# from app.factories.validation_depends.ticket_tag_association import (
#     get_association_validation,
# )


def get_ticket_tags_association_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    # valid_asssociation: AssociationValidation = Depends(
    #     get_association_validation
    # ),
    user: UserRead = Depends(current_active_user),
) -> TicketTagAssociationService:
    return TicketTagAssociationService(
        session=session,
        # valid_asssociation=valid_asssociation,
        user=user,
    )
