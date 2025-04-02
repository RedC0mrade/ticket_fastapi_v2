import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.auth.schemas import UserRead
from app.core.models.base_model import Base
from app.core.models.user import UserAlchemyModel
from app.validators.user import UserValidation


@pytest.fixture(scope="function")
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def empty_db(session: AsyncSession):
    """Очищает базу перед тестом"""
    await session.execute(delete(UserAlchemyModel))
    await session.commit()


# @pytest.fixture(scope="function")
# def user_validation(session):
#     return UserValidation(session)


@pytest.fixture(scope="function")
async def first_user(session: AsyncSession) -> UserRead:

    user = UserAlchemyModel(
        id=1,
        username="first_user",
        hashed_password="123",
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
async def second_user(session: AsyncSession):

    user = UserAlchemyModel(
        id=2,
        username="second_user",
        hashed_password=b"password",
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


# @pytest.fixture(scope="function")
# async def first_user_current_auth(
#     first_user: UserBase,
#     session: AsyncSession,
# ):
#     def mock_user():
#         return first_user

#     return mock_user
