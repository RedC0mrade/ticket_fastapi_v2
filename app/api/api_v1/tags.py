from typing import List
from fastapi import APIRouter, Depends

from app.api.dependencies.current_users_depends import current_active_superuser
from app.core.auth.schemas import UserRead
from app.core.schemas.tag import CreateTag, Tag
from app.crud.tags import TagService
from app.factories.tag import get_tag_service


router = APIRouter(tags=["tags"])


@router.get("/", response_model=List[Tag])
async def get_all_tags(tag_service: TagService = Depends(get_tag_service)):
    return await tag_service.get_all_tags()


@router.get("/get_tag/{tag_id}", response_model=Tag)
async def get_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
):
    return await tag_service.get_tag(tag_id=tag_id)


@router.post("/create_tag", response_model=list[Tag])
async def create_tag(
    tags_in: list[CreateTag],
    tag_service: TagService = Depends(get_tag_service),
    _: UserRead = Depends(current_active_superuser),
):
    return await tag_service.create_tags(tags_in=tags_in)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
    _: UserRead = Depends(current_active_superuser),
):
    return await tag_service.delete_tag(tag_id=tag_id)
