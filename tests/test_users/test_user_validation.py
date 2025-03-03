from fastapi import HTTPException
import pytest
from app.core.models.user import UserAlchemyModel, UserRoleEnum
from app.validators.user import UserValidation


@pytest.mark.order(1)
async def test_valid_user(
    first_user: UserAlchemyModel,
    user_validation: UserValidation,
):
    user: UserAlchemyModel = await user_validation.validate_user(
        user_id=first_user.id
    )
    assert user.id == first_user.id
    assert user.username == "first_user"
    assert user.email == "first_user@mail.ru"
    assert user.user_role == UserRoleEnum.USER


@pytest.mark.order(2)
async def test_not_valid_user(
    user_validation: UserValidation,
):
    with pytest.raises(HTTPException) as excinfo:
        await user_validation.validate_user(user_id=999)
    assert excinfo.value.status_code == 404
