from fastapi import APIRouter

from app.api.dependencies.current_users_depends import fastapi_users
from app.api.dependencies.authentication import authentication_backend
from app.core.auth.schemas import (
    UserRead,
    UserCreate,
)

router = APIRouter(
    tags=["auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    ),
)


# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
