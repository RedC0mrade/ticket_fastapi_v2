from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UserService
from app.core.schemas.user import User, UserWithId, UserPatch
from app.core.models.engine import db_helper
from app.authentication.actions import current_auth_user

router = APIRouter(tags=["Users"])


def get_user_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserService:
    """Зависимость для получения экземпляра UserService."""
    return UserService(session=session)


@router.get("/", response_model=list[UserWithId])
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_users()


@router.get("/me", response_model=UserWithId)
def get_me(user: User = Depends(current_auth_user)):
    return user


@router.get("/{user_id}", response_model=UserWithId)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user(user_id)


@router.post("/", response_model=UserWithId, status_code=201)
async def create_user(
    user_create: User,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user(user_create)


@router.put("/{user_id}", response_model=User)
async def put_user(
    user_id: int,
    user_in: User,
    user_service: UserService = Depends(get_user_service),
):
    result: dict = await user_service.put_user(
        user_in=user_in, user_id=user_id
        )
    return Response(status_code=200, content=f"data changed {result}")


@router.patch("/{user_id}", response_model=User)
async def patch_user(
    user_id: int,
    user_in: UserPatch,
    user_service: UserService = Depends(get_user_service),
):
    result: dict = await user_service.patch_user(
        user_in=user_in, user_id=user_id
    )
    return Response(status_code=200, content=f"data changed {result}")


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id=user_id)
    return Response(status_code=204)
