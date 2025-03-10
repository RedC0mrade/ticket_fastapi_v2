from fastapi_users.authentication import BearerTransport

from core.config import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.api.v1.bearer_token_url,
)