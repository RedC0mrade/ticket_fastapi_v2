from typing import List
from fastapi import HTTPException
from sqlalchemy import Result, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.tag import CreateTag
from app.core.models.tag import TagAlchemyModel
from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)
from app.core.models.ticket import TicketAlchemyModel
from app.core.schemas.user import UserBase
from app.validators.tag import (
    validate_tag,
    validate_tags_in_base,
)
from app.validators.ticket import validate_ticket


class TagService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all_tags(self) -> list[TagAlchemyModel]:
        stmt = select(TagAlchemyModel)
        result: Result = await self.session.execute(stmt)
        tags = result.scalars().all()
        return list(tags)

    async def create_tag(
        self,
        tag_in: CreateTag,
    ) -> TagAlchemyModel:
        tag = TagAlchemyModel(
            tag_name=tag_in.tag_name,
            tag_color=tag_in.tag_color,
        )
        self.session.add(tag)
        await self.session.commit()
        return tag

    async def delete_tag(self, tag_id: int) -> None:
        tag: TagAlchemyModel = await validate_tag(
            tag_id=tag_id,
            session=self.session,
        )
        await self.session.delete(tag)
        await self.session.commit()
