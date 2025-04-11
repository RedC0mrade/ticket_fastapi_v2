import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.schemas import UserRead
from app.core.models.ticket import TicketAlchemyModel
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
        first_user_ticket_to_second: TicketAlchemyModel,
        second_user_ticket_to_first: TicketAlchemyModel,
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

    async def test_get_my_tasks(self):
        tickets = await self.ticket_service.get_my_tasks()
        assert len(tickets) == 1
        assert tickets[0].messages[0].message == "message #1"
        assert tickets[0].acceptor_id == self.second_user.id
        assert tickets[0].amount == 2
        assert tickets[0].executor_id == self.first_user.id
        assert len(tickets[0].tags) == 2
        assert tickets[0].tags[0].tag_name == "White"
        assert tickets[0].tags[0].tag_color == "#000000"
        assert tickets[0].tags[1].tag_name == "Black"
        assert tickets[0].tags[1].tag_color == "#000001"

    async def test_get_my_tickets(self):
        tickets = await self.ticket_service.get_my_tickets()
        assert len(tickets) == 1
        assert tickets[0].messages[0].message == "message #2"
        assert tickets[0].acceptor_id == self.first_user.id
        assert tickets[0].amount == 20
        assert tickets[0].executor_id == self.second_user.id
        assert len(tickets[0].tags) == 2
        assert tickets[0].tags[0].tag_name == "White"
        assert tickets[0].tags[0].tag_color == "#000000"
        assert tickets[0].tags[1].tag_name == "Black"
        assert tickets[0].tags[1].tag_color == "#000001"
