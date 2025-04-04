import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.user import UserAlchemyModel


@pytest.fixture(scope="function")
async def first_user(session: AsyncSession) -> UserRead:

    user = UserAlchemyModel(
        id=1,
        username="first_user",
        hashed_password="111",
        email="first_user@mail.ru",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    session.add(user)
    await session.flush()
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def second_user(session: AsyncSession) -> UserRead:

    user = UserAlchemyModel(
        id=2,
        username="second_user",
        hashed_password="222",
        email="second_user@mail.ru",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    session.add(user)
    await session.flush()
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def super_user(session: AsyncSession) -> UserRead:

    user = UserAlchemyModel(
        id=3,
        username="second_user",
        hashed_password="333",
        email="second_user@mail.ru",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    session.add(user)
    await session.flush()
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def empty_db(session: AsyncSession):
    """Очищает базу перед тестом"""
    await session.execute(delete(UserAlchemyModel))
    await session.commit()
