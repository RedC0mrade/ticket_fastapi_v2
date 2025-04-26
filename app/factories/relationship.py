from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.crud.relatonship import RelationshipService

# from app.factories.blacklist import get_blacklist_validation
from app.factories.database import db_helper

# from app.factories.validation_depends.user import get_validation_user
# from app.factories.validation_depends.relationship import (
#     get_relationship_validation,
# )


def get_relationship_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
    # valid_blacklict: BlacklistValidation = Depends(get_blacklist_validation),
    # valid_relationship: RelationshipValidation = Depends(
    #     get_relationship_validation
    # ),
    # valid_user: UserValidation = Depends(get_validation_user),
) -> RelationshipService:
    return RelationshipService(
        session=session,
        user=user,
    )
