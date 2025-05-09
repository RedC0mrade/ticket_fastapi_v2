import logging
import re
import httpx
from fastapi_users import FastAPIUsers
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.crud.users import UserService
from app.factories.user import get_user_service
from app.utils.templates import templates
from starlette.status import HTTP_303_SEE_OTHER
from app.core.models.user import UserAlchemyModel
from app.api.dependencies.current_users_depends import current_optional_user


router = APIRouter()


class TokenInterceptor(logging.Handler):
    def __init__(self):
        super().__init__()
        self.token = None

    def emit(self, record):
        msg = record.getMessage()
        if "Verification token:" in msg:
            match = re.search(r"Verification token: '(.+?)'", msg)
            if match:
                self.token = match.group(1)


token_handler = TokenInterceptor()
logging.getLogger().addHandler(token_handler)


@router.get("/")
async def users_list(
    request: Request,
    user: UserAlchemyModel | None = Depends(current_optional_user),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_users()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"users": users, "user": user},
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
    name="login",
)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "users/login.html",
        {"request": request},
    )


@router.post(
    "/login",
    response_class=HTMLResponse,
)
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    json = {
        "username": email,
        "password": password,
    }
    async with httpx.AsyncClient(base_url=str(request.base_url)) as client:
        response = await client.post(
            "/api/ticket/v1/auth/login",
            data=json,
        )
        # if response.status_code == 200:
        #     return RedirectResponse(
        #         url="/",
        #         status_code=HTTP_303_SEE_OTHER,
        #     )
        if response.status_code == 204:
            # Token сохранен в cookie, можно перенаправлять
            redirect = RedirectResponse(
                url="/",
                status_code=HTTP_303_SEE_OTHER,
            )
            # Переносим Set-Cookie из ответа на клиент
            for cookie in response.cookies.jar:
                redirect.set_cookie(
                    key=cookie.name,
                    value=cookie.value,
                    expires=cookie.expires,
                    path=cookie.path,
                    domain=cookie.domain,
                    secure=cookie.secure,
                    httponly=cookie.has_nonstandard_attr("HttpOnly"),
                    samesite="Lax",
                )
            return redirect
    
    error = "Неверный email или пароль"
    return templates.TemplateResponse(
        "users/login.html",
        {"request": request, "error": error, "email": email},
        status_code=400,
    )


@router.get(
    "/register_form",
    response_class=HTMLResponse,
    name="register_user",
)
async def register_form_page(request: Request):
    return templates.TemplateResponse(
        "users/register.html", {"request": request}
    )


@router.post("/register_form", response_class=HTMLResponse)
async def register_form_proxy(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    """In order not to change the internal
    logic of fastapi users, the check
    was automated."""

    json_payload = {
        "username": username,
        "email": email,
        "password": password,
    }

    async with httpx.AsyncClient(base_url=str(request.base_url)) as client:
        response = await client.post(
            "/api/ticket/v1/auth/register",
            json=json_payload,
        )

    if response.status_code == 201:
        json_payload = {
            "email": email,
        }
        async with httpx.AsyncClient(base_url=str(request.base_url)) as client:
            response = await client.post(
                "/api/ticket/v1/auth/request-verify-token",
                json={"email": email},
            )

            token = token_handler.token

            response = await client.post(
                "/api/ticket/v1/auth/verify",
                json={"token": token},
            )

        return RedirectResponse(
            url="/",
            status_code=HTTP_303_SEE_OTHER,
        )
    else:
        try:
            error_detail = response.json().get(
                "detail",
                "Ошибка регистрации",
            )
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
