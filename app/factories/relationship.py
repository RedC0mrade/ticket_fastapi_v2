from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.relatonship import RelationshipService
from app.factories.blacklist import get_blacklist_validation
from app.factories.database import db_helper
from app.factories.user import get_validation_user
from app.factories.validation_depends.relationship import (
    get_relationship_validation,
)
from app.validators.blacklist import BlacklistValidation
from app.validators.relationship import RelationshipValidation
from app.validators.user import UserValidation


def get_relationship_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: UserBase = Depends(current_auth_user),
    valid_blacklict: BlacklistValidation = Depends(get_blacklist_validation),
    valid_relationship: RelationshipValidation = Depends(
        get_relationship_validation
    ),
    valid_user: UserValidation = Depends(get_validation_user),
) -> RelationshipService:
    return RelationshipService(
        session=session,
        user=user,
        valid_blacklict=valid_blacklict,
        valid_relationship=valid_relationship,
        valid_user=valid_user,
    )
