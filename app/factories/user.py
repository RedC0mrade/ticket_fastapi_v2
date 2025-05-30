from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.crud.users import UserService
from app.factories.database import db_helper


def get_user_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserService:
    """Фабрика для получения экземпляра UserService."""
    return UserService(session=session)
