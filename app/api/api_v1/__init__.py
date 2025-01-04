from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix=settings.api.v1)

router.include_router(user.)