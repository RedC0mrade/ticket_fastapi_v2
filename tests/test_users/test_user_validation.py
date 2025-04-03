from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation


@pytest.mark.order(1)
async def test_valid_user(
    first_user: UserAlchemyModel,
    session: AsyncSession,
):

    user: UserAlchemyModel = await UserValidation.validate_user(
        session=session, user_id=first_user.id
    )
    assert user.id == first_user.id
    assert user.username == "first_user"
    assert user.email == "first_user@mail.ru"


@pytest.mark.order(2)
async def test_not_valid_user(
    session: AsyncSession
):
    with pytest.raises(HTTPException) as excinfo:
        await UserValidation.validate_user(session=session, user_id=999,)
    assert excinfo.value.status_code == 404
