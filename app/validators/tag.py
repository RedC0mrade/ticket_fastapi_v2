from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.tag import TagAlchemyModel


class TagValidation:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def validate_tags_in_base(
        self,
        tags: list | set,
    ):
        stmt = select(TagAlchemyModel.id).where(TagAlchemyModel.id.in_(tags))
        result: Result = await self.session.execute(stmt)
        tags_in_base = result.scalars().all()

        mising_tags = [tag for tag in tags if tag not in tags_in_base]
        if mising_tags:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wrong tag id: {", ".join(map(str, mising_tags))}",
            )

    async def validate_tag(
        self,
        tag_id: int,
    ) -> TagAlchemyModel:
        tag = await self.session.get(
            TagAlchemyModel,
            tag_id,
        )

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tag {tag_id} not found",
            )
        return tag
