from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation


async def test_valid_user(
    first_user: UserAlchemyModel,
    uservalidation: UserValidation,
):
    user: UserAlchemyModel = await uservalidation.validate_user(
        user_id=first_user.id
    )
    assert user.id == first_user.id
    assert user.username == "first_user"
    assert user.email == "first_user@mail.ru"
    assert user.user_role == "user"
