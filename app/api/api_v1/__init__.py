from fastapi import APIRouter

from app.core.config import settings
from .users import router as user_router
from .messages import router as messages_router
from .tickets import router as tickets_router
from .tags import router as tag_router
from .relationship import router as relationship_router
from .blacklist import router as blacklist_router
from .ticket_tag_association import router as association_router
from .test import router as test_router
from app.authentication.views import router as auth_router
from app.core.auth.manage import fastapi_users
from app.core.auth.backend import auth_backend

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    test_router,
    prefix=settings.api.v1.test,
)
router.include_router(
    user_router,
    prefix=settings.api.v1.users,
)
router.include_router(
    blacklist_router,
    prefix=settings.api.v1.blacklist,
)
router.include_router(
    messages_router,
    prefix=settings.api.v1.messages,
)
router.include_router(
    tickets_router,
    prefix=settings.api.v1.tickets,
)
router.include_router(
    tag_router,
    prefix=settings.api.v1.tags,
)
router.include_router(
    association_router,
    prefix=settings.api.v1.ticket_tag_associations,
)
router.include_router(
    relationship_router,
    prefix=settings.api.v1.relationship,
)
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
