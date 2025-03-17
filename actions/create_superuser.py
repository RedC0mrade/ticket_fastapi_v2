import asyncio
import contextlib
from os import getenv
from fastapi_users.exceptions import UserAlreadyExists

from app.api.dependencies.authentication import get_users_db
from app.api.dependencies.authentication import get_user_manager
from app.core.auth.schemas import UserCreate
from app.core.auth.user_manager import UserManager

from app.core.models import (
    db_helper,
    UserAlchemyModel,
)



get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

default_username = getenv("DEFAULT_USERNAME", "admin")
default_email = getenv("DEFAULT_EMAIL", "admin@admin.com")
default_password = getenv("DEFAULT_PASSWORD", "2121")
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> UserAlchemyModel:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )
    return user


async def create_superuser(
    username:str = default_username,
    email: str = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        username=username,
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )

if __name__ == "__main__":
    try:
        asyncio.run(create_superuser())
    except UserAlreadyExists:
        raise