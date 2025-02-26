from fastapi import APIRouter, Depends

from app.authentication.actions import check_role
from app.core.models.user import UserRoleEnum
from app.core.schemas.user import UserBase
from app.crud.users import UserService
from app.factories.user import get_user_service

router = APIRouter(tags=["test"])


@router.get("/me", response_model=UserBase)
def get_me(
    user_id: int = 0,
    user: UserBase = Depends(
        check_role(
            [
                UserRoleEnum.ADMIN,
                UserRoleEnum.SUPER_USER,
                UserRoleEnum.USER,
            ]
        )
    ),
    user_service: UserService = Depends(get_user_service),
):
    if user_id:
        return await user_service.get_user(user_id=user_id)
    return await user_service.get_user(user_id=user.id)
