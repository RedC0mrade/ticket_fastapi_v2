from fastapi import APIRouter

from app.api.dependencies.current_users_depends import fastapi_users_cookie
from app.api.dependencies.authentication import (
    authentication_backend_cookie_transport,
)
from app.core.auth.schemas import UserRead, UserUpdate


router = APIRouter(
    tags=["cookie"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users_cookie.get_auth_router(
        authentication_backend_cookie_transport,
        requires_verification=True,
    ),
)

# "/me"
# "/{id}"
router.include_router(
    router=fastapi_users_cookie.get_users_router(
        UserRead,
        UserUpdate,
    )
)
