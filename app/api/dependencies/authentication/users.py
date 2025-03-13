from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from app.core.models import (
    db_helper,
    UserAlchemyModel,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield UserAlchemyModel.get_db(session=session)
