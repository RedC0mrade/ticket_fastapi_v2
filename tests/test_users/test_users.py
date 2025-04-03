from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import UserAlchemyModel
from app.core.auth.schemas import UserRead
from app.factories.user import UserService
from app.validators.user import UserValidation


class TestUserService:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        first_user: UserRead,
        second_user: UserRead,
    ):
        self.session = session
        self.first_user = first_user
        self.second_user = second_user
        self.user_service = UserService(
            self.session,
        )

    async def test_get_users(self):

        users = await self.user_service.get_users()
        assert len(users) == 2
        assert users[0].id == 1
        assert users[0].username == "first_user"
        assert users[0].email == "first_user@mail.ru"
        assert users[1].id == 2
        assert users[1].username == "second_user"
        assert users[1].email == "second_user@mail.ru"

    async def test_no_users_in_base(self, empty_db):

        users = await self.user_service.get_users()
        assert len(users) == 0
        assert users == list()

    async def test_delete_user(
        self,
        first_user,
        second_user,
    ):
        users = await self.user_service.get_users()
        assert len(users) == 2
        await self.user_service.delete_user(first_user.id)
        users = await self.user_service.get_users()
        assert len(users) == 1
        assert users[0].username == "second_user"
