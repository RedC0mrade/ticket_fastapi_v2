import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
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
def uservalidation(session):
    return UserValidation(session)


@pytest.fixture(scope="function")
async def first_user(session: AsyncSession):

    user = UserAlchemyModel(
        id=1,
        username="first_user",
        password=b"password",
        email="first_user@mail.ru",
    )

    session.add(user)
    await session.commit()
    return user


@pytest.fixture(scope="function")
async def second_user(session: AsyncSession):

    user = UserAlchemyModel(
        id=2,
        username="second_user",
        password=b"password",
        email="second_user@mail.ru",
    )

    session.add(user)
    await session.commit()
    return user
