import asyncio
import contextlib
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

default_username = ("first", "second")
default_email = ("first@first.com", "second@second.com")
default_password = "111"
default_is_active = True
default_is_superuser = False
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


async def create_users(
    username: list = default_username,
    email: list = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    for value in range(len(username)):
        user_create = UserCreate(
            username=username[value],
            email=email[value],
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
        asyncio.run(create_users())
    except UserAlreadyExists:
        raise
