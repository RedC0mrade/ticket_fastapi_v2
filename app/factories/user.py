from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.schemas.user import UserBase
from app.crud.users import UserService
from app.factories.database import db_helper
from app.factories.validation_depends.user import get_validation_user
from app.validators.user import UserValidation


def get_user_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_user: UserValidation = Depends(get_validation_user),
    # user: UserBase = 
) -> UserService:
    """Фабрика для получения экземпляра UserService."""
    return UserService(
        session=session,
        valid_user=valid_user,
    )
