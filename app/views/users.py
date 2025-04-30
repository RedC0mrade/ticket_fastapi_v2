from fastapi import APIRouter, Depends, Request

from app.crud.users import UserService
from app.factories.user import get_user_service
from app.utils.templates import templates

router = APIRouter()


@router.get("/")
async def users_list(
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_users()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"users": users},
    )


@router.post("/registration")
async def registration(
    request: Request,
):
    pass
