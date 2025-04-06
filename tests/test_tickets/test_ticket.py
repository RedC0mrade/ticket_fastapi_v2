import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.crud.messages import MessageService
from app.crud.tickets import TicketService


class TestTicketService:

    @pytest.fixture(
        scope="function",
        autouse=True,
    )
    async def setup(
        self,
        session: AsyncSession,
        first_user: UserRead,
        second_user: UserRead,
    ):
        self.session = session
        self.first_user = first_user
        self.second_user = second_user
        self.message_service: MessageService = MessageService(
            session=self.session,
            user=self.first_user,
        )
        self.ticket_service: TicketService = TicketService(
            session=self.session,
            user=self.first_user,
            message_service=self.message_service,
        )

    async def tast_get_my_tasks(self):
        await