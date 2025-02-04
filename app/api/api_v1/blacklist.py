from fastapi import APIRouter, Depends

from app.factories.blacklist import get_blacklist_service
from app.core.schemas.black import BlackUser, BlacklistUser
from app.crud.black import BlacklistServices


router = APIRouter(tags=["blacklist"])


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
