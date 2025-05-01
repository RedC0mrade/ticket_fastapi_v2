from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse

from app.api.dependencies.authentication.user_manager import get_user_manager
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


@router.get("/register", name="register_user")
async def register_get(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})

@router.post("/register", name="register_user")
async def register_post(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    user_manager=Depends(get_user_manager),
):
    try:
        user = await user_manager.create(
            {
                "email": email,
                "password": password,
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "username": username,
            }
        )
        # Редирект на страницу входа или главную
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    except Exception as err:
        return templates.TemplateResponse(
            "users/register.html",
            {
                "request": request,
                "error": str(err),
            },
            status_code=400
        )