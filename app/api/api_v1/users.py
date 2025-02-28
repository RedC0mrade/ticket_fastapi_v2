from fastapi import APIRouter, Response, Depends

from app.crud.users import UserService
from app.core.schemas.user import User, UserBase, UserPatch
from app.authentication.actions import current_auth_user
from app.factories.user import get_user_service

router = APIRouter(tags=["Users"])


@router.get("/all_users", response_model=list[UserBase])
async def get_users(
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users()


@router.get("/me", response_model=UserBase)
def get_me(
    user: UserBase = Depends(current_auth_user),
):
    return user


@router.get("/", response_model=UserBase)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user(user_id=user_id)


@router.post("/", response_model=UserBase, status_code=201)
async def create_user(
    user_create: User,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user(user_create)


@router.put("/", response_model=UserBase)
async def put_user(
    user_in: User,
    user_service: UserService = Depends(get_user_service),
    user: UserBase = Depends(current_auth_user),
):

    return await user_service.put_user(
        user_in=user_in,
        user_id=user.id,
    )


@router.patch("/", response_model=UserBase)
async def patch_user(
    user_in: UserPatch,
    user_service: UserService = Depends(get_user_service),
    user: UserBase = Depends(current_auth_user),
):
    result: dict = await user_service.patch_user(
        user_in=user_in, user_id=user.id
    )
    return Response(status_code=200, content=f"data changed {result}")


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id=user_id)
    return Response(status_code=204)
