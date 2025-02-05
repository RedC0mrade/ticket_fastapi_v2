from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.crud.users import UserService
from app.factories.database import db_helper
from app.validators.user import UserValidation


def get_validation_user(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserValidation:
    """Фабрика для получения экземпляра валидатора пользователя"""
    return UserValidation(session)


def get_user_service(
    session: AsyncSession = Depends(db_helper.session_getter),
    valid_user: UserValidation = Depends(get_validation_user),
) -> UserService:
    """Фабрика для получения экземпляра UserService."""
    return UserService(
        session=session,
        valid_user=valid_user,
    )
