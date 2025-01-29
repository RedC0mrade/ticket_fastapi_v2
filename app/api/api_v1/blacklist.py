from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.authentication.actions import current_auth_user
from app.core.models.engine import db_helper
from app.core.schemas.black import BlackUser, BlacklistUser
from app.core.schemas.user import User
from app.crud.black import BlacklistServices


router = APIRouter(tags=["blacklist"])


def get_blacklist_service(
    user: User = Depends(current_auth_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return BlacklistServices(
        user=user,
        session=session,
    )


@router.get(
    "/my_blacklist",
    response_model=list[BlacklistUser],
)
async def get_all_blacklist_users(
    black_service: BlacklistServices = Depends(get_blacklist_service),
):
    return await black_service.get_all_blacklist_users()


@router.delete(
    "/remove_from_blacklist/{black_id}",
    status_code=204,
)
async def remove_from_blacklist(
    black_id: int,
    black_service: BlacklistServices = Depends(get_blacklist_service),
):
    return await black_service.remove_from_blacklist(black_id=black_id)


@router.post(
    "/add_to_blacklist/{black_id}",
    # response_model=BlackUser,
    # status_code=201,
)
async def add_to_blacklist(
    black_id: int,
    black_service: BlacklistServices = Depends(get_blacklist_service),
):
    return await black_service.add_to_blacklist(black_id=black_id)
