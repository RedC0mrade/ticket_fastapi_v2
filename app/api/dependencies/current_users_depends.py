from fastapi_users import FastAPIUsers

from app.core.models import UserAlchemyModel

from app.api.dependencies.authentication import get_user_manager
from app.api.dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers[UserAlchemyModel, int](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(
    active=True,
    superuser=True,
)
current_optional_user = fastapi_users.current_user(optional=True)
