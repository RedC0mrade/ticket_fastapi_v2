from fastapi import APIRouter, Depends
from typing import List

from app.api.dependencies.current_users_depends import current_active_user
from app.core.auth.schemas import UserRead
from app.core.models.user import UserAlchemyModel
from app.factories.user import get_user_service
from app.crud.users import UserService


router = APIRouter(tags=["Users"])


@router.get(
    "/all_users",
    response_model=list[UserRead],
)
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> List[UserAlchemyModel]:
    return await user_service.get_users()


@router.delete("/self")
async def delete_your_profile(
    user_service: UserService = Depends(get_user_service),
    user: UserRead = Depends(current_active_user),
):
    return await user_service.delete_user(user_id=user.id)
