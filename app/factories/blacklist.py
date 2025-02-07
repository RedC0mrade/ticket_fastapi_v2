from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.schemas.user import UserBase
from app.crud.black import BlacklistServices
from app.factories.database import db_helper
from app.factories.validation_depends.blacklist import get_blacklist_validation
from app.factories.validation_depends.relationship import (
    get_relationship_validation,
)
from app.validators.blacklist import BlacklistValidation
from app.validators.relationship import RelationshipValidation


def get_blacklist_service(
    user: UserBase = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_blacklict: BlacklistValidation = Depends(get_blacklist_validation),
    valid_relationship: RelationshipValidation = Depends(
        get_relationship_validation
    ),
) -> BlacklistValidation:
    return BlacklistServices(
        user=user,
        session=session,
        valid_blacklict=valid_blacklict,
        valid_relationship=valid_relationship,
    )
