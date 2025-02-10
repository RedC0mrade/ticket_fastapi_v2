from fastapi import APIRouter, Response, Depends

from app.core.models.user import UserRoleEnum
from app.core.schemas.user import User, UserBase, UserPatch
from app.permission.admin_permission import check_role

router = APIRouter(tags=["test"])

@router.get("/me", response_model=UserBase)
def get_me(
    user: UserBase = Depends(check_role([UserRoleEnum.ADMIN, UserRoleEnum.SUPER_USER])),
):
    return user