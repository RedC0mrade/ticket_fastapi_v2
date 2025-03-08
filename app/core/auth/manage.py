from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.factories.database import db_helper
from app.core.models.user import UserAlchemyModel
from app.core.auth.backend import auth_backend
from app.core.auth.schemas import UserRead, UserCreate, UserUpdate


async def get_user_db(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    yield SQLAlchemyUserDatabase(session, UserAlchemyModel)


fastapi_users = FastAPIUsers[UserAlchemyModel, int](
    get_user_db,
    [auth_backend],
    UserAlchemyModel,
    UserCreate,
    UserUpdate,
    UserRead,
)
