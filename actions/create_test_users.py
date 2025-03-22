import asyncio
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user import UserAlchemyModel
from app.core.models import db_helper


async def create_test_users(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    stmt = [
        UserAlchemyModel(
            username="first",
            email="first@first.com",
            password="111",
        ),
        UserAlchemyModel(
            username="second",
            email="second@second.com",
            password="111",
        ),
    ]
    session.add_all(stmt)
    session.commit()

async def main():
    async with db_helper.session_factory() as session:
        await create_test_users(session=session)

if __name__ == "__main__":
    asyncio.run(main())