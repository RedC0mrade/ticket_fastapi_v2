import uvicorn
from fastapi import FastAPI

from fastapi.concurrency import asynccontextmanager

from app.core.config import settings
from app.api import router as api_router
from app.core.models import db_helper


@asynccontextmanager
async def lifepan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifepan)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
