import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.tag import Tag
from app.crud.tags import TagService
from app.core.schemas.tag import CreateTag


class TestTagsService:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        tag_white: Tag,
        tag_black: Tag,
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
        tags = [
            CreateTag(tag_name="Rose", tag_color="#000002"),
            CreateTag(tag_name="Grey", tag_color="#000003"),
        ]
        await self.tag_service.create_tags(tags_in=tags)
        tags_in_base = await self.tag_service.get_all_tags()

        assert len(tags_in_base) == 4
        assert tags_in_base[2].tag_name == "Rose"
        assert tags_in_base[3].tag_name == "Grey"

    async def test_delete_tag(self):
        tags_in_base = await self.tag_service.get_all_tags()
        assert len(tags_in_base) == 2
        await self.tag_service.delete_tag(tag_id=self.tag_white.id)
        tags_in_base = await self.tag_service.get_all_tags()
        assert len(tags_in_base) == 1
        assert tags_in_base[0].tag_name == "Black"
