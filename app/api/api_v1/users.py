from fastapi import APIRouter, Depends
from app.core.config import settings

from app.api.dependencies.current_users_depends import fastapi_users
from app.core.auth.schemas import UserRead, UserUpdate
from app.crud.users import UserService
from app.factories.user import get_user_service

router = APIRouter(tags=["Users"])

# "/me"
# "/{id}"
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    )
)

user_router = APIRouter(tags=["test"], prefix=settings.api.v1.test)


@user_router.get(
    "/all_users",
    response_model=list[UserRead],
)
async def get_users(
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users()


# @router.delete(
#     "/{user_id}",
#     status_code=204,
# )
# async def delete_user(
#     user: UserRead = Depends(current_active_user),
#     user_service: UserService = Depends(get_user_service),
# ):
#     await user_service.delete_user(user_id=user.id)
#     return Response(status_code=204)
