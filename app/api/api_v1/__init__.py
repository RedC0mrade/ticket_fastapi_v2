from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.core.config import settings
from .auth import router as auth_router
from .blacklist import router as blacklist_router
from .messages import router as messages_router
from .tags import router as tag_router
from .tickets import router as tickets_router
from .ticket_tag_association import router as association_router
from .relationship import router as relationship_router
from .users import router as users_router
from .test import router as test_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
router.include_router(
    users_router,
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
    test_router,
    prefix=settings.api.v1.test,
)
