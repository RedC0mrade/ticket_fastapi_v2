import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.tag import TagAlchemyModel


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
