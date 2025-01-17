from fastapi import APIRouter

from app.core.config import settings
from .users import router as user_router
from .messages import router as messages_router
from .tickets import router as tickets_router
from .tags import router as tag_router
from .ticket_tag_association import router as association_router
from app.authentication.views import router as auth_router

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(
    user_router,
    prefix=settings.api.v1.users,
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
    auth_router,
    prefix=settings.api.v1.auth,
)
