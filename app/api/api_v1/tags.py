from typing import List
from fastapi import APIRouter, Depends

from app.authentication.actions import check_role
from app.core.models.user import UserRoleEnum
from app.core.schemas.tag import CreateTag, Tag
from app.core.schemas.user import UserBase
from app.crud.tags import TagService
from app.factories.tag import get_tag_service


router = APIRouter(tags=["tags"])


@router.get("/", response_model=List[Tag])
async def get_all_tags(tag_service: TagService = Depends(get_tag_service)):
    return await tag_service.get_all_tags()


@router.post("/create_tag", response_model=Tag)
async def create_tag(
    tag_in: CreateTag,
    tag_service: TagService = Depends(get_tag_service),
    user: UserBase = Depends(
        check_role([UserRoleEnum.ADMIN, UserRoleEnum.SUPER_USER])
    ),
):
    return await tag_service.create_tag(tag_in=tag_in)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: int,
    tag_service: TagService = Depends(get_tag_service),
    user: UserBase = Depends(
        check_role(
            [
                UserRoleEnum.ADMIN,
                UserRoleEnum.SUPER_USER,
            ]
        )
    ),
):

    return await tag_service.delete_tag(tagt_id=tag_id)
