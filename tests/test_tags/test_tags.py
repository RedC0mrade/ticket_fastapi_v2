import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.tag import Tag
from app.crud.tags import TagService


class TestTagsService:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        tag_white: Tag,
        tag_black,
    ):
        self.session = session
        self.tag_white = tag_white
        self.tag_black = tag_black
        self.tag_service = TagService(session=self.session)

    async def test_get_all_tags(self):
        tags = await self.tag_service.get_all_tags()
        assert len(tags) == 2
        assert tags[0].tag_name == "White"
        assert tags[0].tag_color == "#000000"
        assert tags[1].tag_name == "Black"
        assert tags[1].tag_color == "#000001"

    async def test_no_tags_in_base(self, emty_db_tags):
        tags = await self.tag_service.get_all_tags()
        assert len(tags) == 0
        assert tags == list()

    async def test_create_tags(self):
        