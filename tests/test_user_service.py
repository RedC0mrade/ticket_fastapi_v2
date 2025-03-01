import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import UserAlchemyModel
from app.factories.user import UserService
from app.validators.user import UserValidation


@pytest.mark.asyncio
async def test_get_users(
    session: AsyncSession,
    uservalidation: UserValidation,
):

    test_users = [
        UserAlchemyModel(
            username="Alice",
            password=b"password",
            email="alice.@mail.com",
        ),
        UserAlchemyModel(
            username="Bob",
            password=b"password",
            email="bob.@mail.com",
        ),
    ]
    session.add_all(test_users)
    await session.commit()

    user_service = UserService(
        session=session,
        valid_user=uservalidation,
    )
    users = await user_service.get_users()
    assert len(users) == 2
    assert users[0].username == "Alice"
    assert users[1].username == "Bob"
