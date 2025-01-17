from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.tag import CreateTag, Tag
from app.core.models.engine import db_helper
from app.crud.tags import TagService


router = APIRouter(tags=["tags"])


def get_tag_service(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TagService:
    return TagService(session=session)


@router.get("/", response_model=List[Tag])
async def get_all_tags(tag_service: TagService = Depends(get_tag_service)):
    return await tag_service.get_all_tags()


@router.post("/create_tag", response_model=Tag)
async def create_tag(
    tag_in: CreateTag,
    tag_service: TagService = Depends(get_tag_service),
):
    return await tag_service.create_tag(tag_in=tag_in)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
):

    try:
        await tag_service.delete_tag(tagt_id=tag_id)
    except:
        return Response(status_code=404, content="tag not found")
