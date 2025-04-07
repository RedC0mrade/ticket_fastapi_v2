import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.auth.schemas import UserRead
from app.core.models.base_model import Base
from app.core.models.message import MessageAlchemyModel
from app.core.models.tag import TagAlchemyModel
from app.core.models.ticket import TicketAlchemyModel
from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)
from app.core.models.user import UserAlchemyModel
from app.core.schemas.tag import Tag


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


@pytest.fixture(scope="function")
async def tag_white(session: AsyncSession):

    tag = TagAlchemyModel(
        tag_name="White",
        tag_color="#000000",
    )
    session.add(tag)
    await session.flush()
    await session.commit()
    await session.refresh(tag)
    return tag


@pytest.fixture(scope="function")
async def tag_black(session: AsyncSession):

    tag = TagAlchemyModel(
        tag_name="Black",
        tag_color="#000001",
    )
    session.add(tag)
    await session.flush()
    await session.commit()
    await session.refresh(tag)
    return tag


@pytest.fixture(scope="function")
async def emty_db_tags(session: AsyncSession):
    await session.execute(delete(TagAlchemyModel))


@pytest.fixture(scope="function")
async def first_user_ticket_to_second(
    first_user: UserRead,
    second_user: UserRead,
    tag_white: Tag,
    tag_black: Tag,
    session: AsyncSession,
):
    ticket: TicketAlchemyModel = TicketAlchemyModel(
        ticket_name="ticket_#1",
        amount=2,
        acceptor_id=second_user.id,
        executor_id=first_user.id,
    )

    session.add(ticket)
    await session.flush()

    message: MessageAlchemyModel = MessageAlchemyModel(
        message="message #1", ticket_id=ticket.id
    )
    session.add(message)

    associations: TicketTagAssociationAlchemyModel = (
        TicketTagAssociationAlchemyModel(
            ticket_id=ticket.id,
            tag_id=tag_white.id,
        )
    )
    session.add(associations)

    associations_two: TicketTagAssociationAlchemyModel = (
        TicketTagAssociationAlchemyModel(
            ticket_id=ticket.id,
            tag_id=tag_black.id,
        )
    )
    session.add(associations_two)
    await session.commit()
    return ticket


@pytest.fixture(scope="function")
async def second_user_ticket_to_first(
    first_user: UserRead,
    second_user: UserRead,
    tag_white: Tag,
    tag_black: Tag,
    session: AsyncSession,
):
    ticket: TicketAlchemyModel = TicketAlchemyModel(
        ticket_name="ticket_#1",
        amount=20,
        acceptor_id=first_user.id,
        executor_id=second_user.id,
    )

    session.add(ticket)
    await session.flush()

    message: MessageAlchemyModel = MessageAlchemyModel(
        message="message #2", ticket_id=ticket.id
    )
    session.add(message)

    associations: TicketTagAssociationAlchemyModel = (
        TicketTagAssociationAlchemyModel(
            ticket_id=ticket.id,
            tag_id=tag_white.id,
        )
    )
    session.add(associations)

    await session.commit()
    return ticket
