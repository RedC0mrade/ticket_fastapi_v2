from fastapi_users.authentication import BearerTransport, CookieTransport

from app.core.config import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)

cookie_transport = CookieTransport(
    cookie_name="my_auth_cookie",
    cookie_max_age=settings.authentification_config.lifetime_seconds,
    cookie_secure=True,
    cookie_httponly=True,
    cookie_samesite="lax",
)
