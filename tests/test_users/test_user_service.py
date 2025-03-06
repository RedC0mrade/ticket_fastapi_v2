from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.models import UserAlchemyModel
from app.core.models.user import UserRoleEnum
from app.core.schemas.user import User, UserBase
from app.factories.user import UserService
from app.validators.user import UserValidation


class TestUserServiсe:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        user_validation: UserValidation,
        first_user: UserBase,
        second_user: UserBase,
    ):
        self.session = session
        self.user_validation = user_validation
        self.first_user = first_user
        self.second_user = second_user
        self.user_service = UserService(
            self.session,
            self.user_validation,
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

    async def test_get_user(self):

        user: UserAlchemyModel = await self.user_service.get_user(1)
        assert user.id == 1
        assert user.username == "first_user"

    async def test_user_with_wrong_id(self):

        with pytest.raises(HTTPException) as exc:
            await self.user_service.get_user(999)
        assert exc.value.status_code == 404
        assert exc.value.detail == "User with id 999 not found"

    async def test_create_user(self, empty_db):
        user_in = User(
            username="user",
            password="password",
            email="user@mail.ru",
        )
        user: UserAlchemyModel = await self.user_service.create_user(user_in)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        assert user.username == "user"
        assert user.id == 1
        assert user.email == "user@mail.ru"
        assert isinstance(user.password, bytes)
        assert user.user_role == UserRoleEnum.USER

    async def test_put_user(self, first_user_current_auth):

        main_app.dependency_overrides[current_auth_user]