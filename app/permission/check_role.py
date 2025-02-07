from fastapi import Depends, HTTPException, status
from app.authentication.actions import current_auth_user
from app.core.models.user import UserAlchemyModel, UserRoleEnum


def check_role(allowed_role: list[UserRoleEnum]):
    def _role_checker(user: UserAlchemyModel = Depends(current_auth_user)):
        if user.user_role not in allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
                )
        return user
    return Depends(_role_checker)
