import uvicorn
from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.concurrency import asynccontextmanager

from app.core.config import settings
from app.api import router as api_router
from app.core.models import db_helper
from app.crud.users import UserService
from app.factories.user import get_user_service
from app.utils.templates import templates


@asynccontextmanager
async def lifepan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifepan)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


@main_app.get("/")
async def users_list(
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    users = await user_service.get_users()
    return templates.TemplateResponse(request=request, name="index.html", context={"users": users})


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
