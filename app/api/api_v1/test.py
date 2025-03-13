# from fastapi import APIRouter, Depends, Query, HTTPException

# from app.authentication.actions import cheak_permission
# from app.core.models.user import UserRoleEnum
# from app.core.schemas.user import UserBase, UserWithRole
# from app.crud.users import UserService
# from app.factories.user import get_user_service

# router = APIRouter(tags=["test"])


# def admin_user_id(
#     user_text: str,
#     user: UserWithRole = Depends(cheak_permission()),
#     user_id: int | None = Query(
#         None, description="ID пользователя (только для администраторов)"
#     ),
# ) -> int:
#     """Функция зависимости: позволяет передавать user_id только администраторам"""
#     if user.user_role == UserRoleEnum.ADMIN and user_id:
#         return user_id
#     return user.id


# @router.get("/me", response_model=UserBase)
# async def get_me(
#     target_user_id: int = Depends(admin_user_id),
#     user_service: UserService = Depends(get_user_service),
# ):
#     return await user_service.get_user(user_id=target_user_id)
