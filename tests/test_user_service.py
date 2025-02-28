import pytest
from unittest.mock import MagicMock
from app.core.models import UserAlchemyModel
from app.factories.user import UserService
from app.validators.user import UserValidation


@pytest.mark.asyncio
async def test_get_users(session, mocker):
    mock_valid_user = MagicMock(UserValidation)

    test_users = [
        UserAlchemyModel(
            id=1,
            username="Alice",
            password=b"password",
            email="alice.@mail.com",
        ),
        UserAlchemyModel(
            id=2,
            username="Bob",
            password=b"password",
            email="bob.@mail.com",
        ),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = test_users
    mocker.patch.object(session, "execute", return_value=mock_result)

    user_service = UserService(session=session, valid_user=mock_valid_user)
    users = await user_service.get_users()
    assert len(users) == 2
    assert users[0].username == "Alice"
    assert users[1].username == "Bob"
