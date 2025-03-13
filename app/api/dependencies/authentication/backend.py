from fastapi_users.authentication import AuthenticationBackend

from app.core.auth.transport import bearer_transport
from app.api.dependencies.authentication.strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
