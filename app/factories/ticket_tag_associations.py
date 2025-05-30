from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.crud.ticket_tag_association import TicketTagAssociationService
from app.factories.database import db_helper




def get_ticket_tags_association_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
) -> TicketTagAssociationService:
    return TicketTagAssociationService(
        session=session,
        user=user,
    )
