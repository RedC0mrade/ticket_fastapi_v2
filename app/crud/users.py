from typing import List

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.actions import current_auth_user
from app.core.models.user import UserAlchemyModel
from app.core.schemas.user import User, UserBase, UserPatch
from app.authentication.password_utils import hash_password
from app.validators.user import UserValidation


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        valid_user: UserValidation,
    ):
        self.session = session
        self.valid_user = valid_user

    async def get_users(self) -> List[UserAlchemyModel]:
        stmt = select(UserAlchemyModel)
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return list(users)

    async def get_user(
        self,
        user_id: int,
    ) -> UserAlchemyModel:
        return await self.valid_user.validate_user(
            user_id=user_id,
        )

    async def create_user(
        self,
        user_in: User,
    ) -> UserAlchemyModel:
        user_in.password = hash_password(user_in.password)
        new_user = UserAlchemyModel(**user_in.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def put_user(
        self,
        user_in: User,
        user: UserBase = Depends(current_auth_user)
    ) -> UserBase:
        user_in.password = hash_password(user_in.password)
        new_values: dict = user_in.model_dump()
        user = (
            update(UserAlchemyModel)
            .where(UserAlchemyModel.id == user.id)
            .values(new_values)
        )
        await self.session.execute(user)
        await self.session.commit()
        user = await self.session.get(UserAlchemyModel, user.id)
        return user

    async def patch_user(
        self,
        user_in: UserPatch,
        user_id: int,
    ) -> dict:
        new_values: dict = user_in.model_dump(exclude_unset=True)
        if new_values.get("password"):
            new_values["password"] = hash_password(user_in.password)
        user = (
            update(UserAlchemyModel)
            .where(UserAlchemyModel.id == user_id)
            .values(new_values)
        )
        await self.session.execute(user)
        await self.session.commit()
        return new_values

    async def delete_user(
        self,
        user_id: int,
    ) -> None:
        user = await self.session.get(
            UserAlchemyModel,
            user_id,
        )
        await self.session.delete(user)
        await self.session.commit()
