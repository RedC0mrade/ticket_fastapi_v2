from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.tag import CreateTag
from app.core.models.tag import TagAlchemyModel

from app.validators.tag import TagValidation


class TagService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all_tags(
        self,
    ) -> list[TagAlchemyModel]:
        stmt = select(TagAlchemyModel)
        result: Result = await self.session.execute(stmt)
        tags = result.scalars().all()
        return list(tags)

    async def get_tag(self, tag_id: int) -> TagAlchemyModel:
        tag = await TagValidation.validate_tag(
            session=self.session,
            tag_id=tag_id,
        )
        return tag

    async def create_tags(
        self,
        tags_in: list[CreateTag],
    ) -> list[TagAlchemyModel]:
        tags = [
            TagAlchemyModel(
                tag_name=tag.tag_name,
                tag_color=tag.tag_color,
            )
            for tag in tags_in
        ]
        self.session.add_all(tags)
        await self.session.commit()
        return tags

    async def delete_tag(
        self,
        tag_id: int,
    ) -> None:
        tag: TagAlchemyModel = await TagValidation.validate_tag(
            tag_id=tag_id,
            session=self.session,
        )
        await self.session.delete(tag)
        await self.session.commit()
