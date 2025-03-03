import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import UserAlchemyModel
from app.factories.user import UserService
from app.validators.user import UserValidation


class TestUserServise:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        user_validation: UserValidation,
    ):
        self.session = session
        self.user_validation = user_validation
        self.user_service = UserService(
            self.session,
            self.user_validation,
        )

    async def test_get_users(self):

        test_users = [
            UserAlchemyModel(
                username="user",
                password=b"password",
                email="user@mail.com",
            ),
            UserAlchemyModel(
                username="user#2",
                password=b"password",
                email="user#2@mail.com",
            ),
        ]
        self.session.add_all(test_users)
        await self.session.commit()

        users = await self.user_service.get_users()
        assert len(users) == 2
        assert users[0].username == "user"
        assert users[0].email == "user@mail.com"
        assert users[1].username == "user#2"
        assert users[1].email == "user#2@mail.com"

    async def test_get_no_users_in_base(self):

        users = await self.user_service.get_users()
        assert len(users) == 0
