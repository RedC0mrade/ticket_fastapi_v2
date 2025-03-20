from fastapi import APIRouter

from app.api.dependencies.current_users_depends import fastapi_users
from app.core.auth.schemas import UserRead, UserUpdate

router = APIRouter(tags=["Users"])
# "/me"
# "/{id}"
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    )
)

# @user_router.get(
#     "/all_users",
#     response_model=list[UserRead],
# )
# async def get_users(
#     user_service: UserService = Depends(get_user_service),
# ):
#     return await user_service.get_users()
