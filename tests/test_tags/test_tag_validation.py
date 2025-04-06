from fastapi import HTTPException
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.tag import TagAlchemyModel
from app.validators.tag import TagValidation


@pytest.mark.asyncio
async def test_tag_validation(
    tag_white: TagAlchemyModel,
    session: AsyncSession,
):

    tag: TagAlchemyModel = await TagValidation.validate_tag(
        session=session,
        tag_id=tag_white.id,
    )
    assert tag.id == tag_white.id
    assert tag.tag_name == tag_white.tag_name
    assert tag.tag_color == tag_white.tag_color


@pytest.mark.asyncio
async def test_no_valid_tag(
    tag_white: TagAlchemyModel,
    session: AsyncSession,
):
    with pytest.raises(HTTPException) as excinfo:
        await TagValidation.validate_tag(
            session=session,
            tag_id=999,
        )
    assert excinfo.value.status_code == 404


@pytest.mark.asyncio
async def test_no_valid_tags_in_base(
    tag_white: TagAlchemyModel,
    tag_black: TagAlchemyModel,
    session: AsyncSession,
):
    await TagValidation.validate_tags_in_base(
            session=session,
            tags=[1, 2],
        )
    with pytest.raises(HTTPException) as excinfo:
        await TagValidation.validate_tags_in_base(
            session=session,
            tags=[1, 2, 3],
        )
    assert excinfo.value.status_code == 404
