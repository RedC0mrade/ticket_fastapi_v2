from fastapi import APIRouter, Depends

from app.authentication.actions import check_role
from app.core.models.user import UserRoleEnum
from app.core.schemas.user import UserBase

router = APIRouter(tags=["test"])


@router.get("/me", response_model=UserBase)
def get_me(
    user: UserBase = Depends(
        check_role([UserRoleEnum.ADMIN, UserRoleEnum.SUPER_USER])
    ),
):
    return user
