from fastapi import HTTPException
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import UserAlchemyModel
from app.core.schemas.user import UserBase
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
        first_user: UserBase,
        second_user: UserBase,
    ):
        self.session = session
        self.user_validation = user_validation
        self.first_usere = first_user
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