from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.authentication.actions import current_auth_user
from app.core.models.engine import db_helper
from app.core.schemas.user import User
from app.crud.black import BlacklistServices

router = APIRouter(tags=["blacklist"])

def blacklist_service(
    user: User = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return BlacklistServices(
        user=user,
        session=session,
    )
