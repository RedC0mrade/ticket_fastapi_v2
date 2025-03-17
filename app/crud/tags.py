from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.current_users_depends import current_active_superuser
from app.core.auth.schemas import UserRead
from app.core.schemas.tag import CreateTag
from app.core.models.tag import TagAlchemyModel

from app.validators.tag import TagValidation


class TagService:
    def __init__(
        self,
        session: AsyncSession,
        valid_tag: TagValidation,
    ):
        self.session = session
        self.valid_tag = valid_tag

    async def get_all_tags(
        self,
    ) -> list[TagAlchemyModel]:
        stmt = select(TagAlchemyModel)
        result: Result = await self.session.execute(stmt)
        tags = result.scalars().all()
        return list(tags)

    async def create_tags(
        self,
        tags_in: list[CreateTag],
        _: UserRead = Depends(current_active_superuser),

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
        _: UserRead = Depends(current_active_superuser),
    ) -> None:
        tag: TagAlchemyModel = await self.valid_tag(
            tag_id=tag_id,
            session=self.session,
        )
        await self.session.delete(tag)
        await self.session.commit()
