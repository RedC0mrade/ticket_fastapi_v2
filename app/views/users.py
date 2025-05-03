import httpx
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.dependencies.authentication.user_manager import get_user_manager
from app.crud.users import UserService
from app.factories.user import get_user_service
from app.utils.templates import templates
from starlette.status import HTTP_303_SEE_OTHER

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

@router.get("/register_form", response_class=HTMLResponse, name="register_user")
async def register_form_page(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})

@router.post("/register_form", response_class=HTMLResponse)
async def register_form_proxy(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    # Формируем JSON-пакет для FastAPI Users
    json_payload = {
        "username": username,
        "email": email,
        "password": password,
    }

    async with httpx.AsyncClient(base_url=str(request.base_url)) as client:
        response = await client.post("/api/ticket/v1/auth/register", json=json_payload)

    if response.status_code == 201:
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    else:
        try:
            error_detail = response.json().get("detail", "Ошибка регистрации")
        except Exception:
            error_detail = "Ошибка регистрации"

        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": error_detail,
                "username": username,
                "email": email,
            },
        )
