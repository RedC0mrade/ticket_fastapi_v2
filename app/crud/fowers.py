from typing import List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.user import UserWithId


class FollowerService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserWithId,
    ):
        self.session = session
        self.user = user

    async def get_followers(self):
        
