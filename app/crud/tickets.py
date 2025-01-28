from typing import List
from sqlalchemy import and_, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core.schemas.user import UserBase
from app.core.models.ticket_tag_association import (
    TicketTagAssociationAlchemyModel,
)
from app.core.schemas.ticket import CreateTicket
from app.core.models.ticket import TicketAlchemyModel
from app.crud.messages import MessageService
from app.validators.tag import validate_tags_in_base
from app.validators.ticket import validate_ticket


class TicketService:
    def __init__(
        self,
        session: AsyncSession,
        user: UserBase,
        message_service: MessageService,
    ):
        self.session = session
        self.user = user
        self.message_service = message_service

    async def get_my_tasks(self) -> List[TicketAlchemyModel]:
        stmt = select(TicketAlchemyModel).where(
            TicketAlchemyModel.executor_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        tickets = result.scalars().all()
        return list(tickets)

    async def get_my_tickets(self) -> List[TicketAlchemyModel]:
        stmt = select(TicketAlchemyModel).where(
            TicketAlchemyModel.acceptor_id == self.user.id
        )
        result: Result = await self.session.execute(stmt)
        tickets = result.scalars().all()
        return list(tickets)

    async def create_ticket(
        self,
        ticket_in: CreateTicket,
    ) -> TicketAlchemyModel:
        if self.user.id == ticket_in.acceptor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't create ticket to your self",
            )

        check_stmt = select(TicketAlchemyModel).where(
            and_(
                TicketAlchemyModel.ticket_name == ticket_in.ticket_name,
                TicketAlchemyModel.acceptor_id == ticket_in.acceptor_id,
                TicketAlchemyModel.executor_id == self.user.id,
            )
        )
        result: Result = await self.session.execute(check_stmt)
        check_ticket: TicketAlchemyModel = result.scalar_one_or_none()

        if check_ticket:
            return await self.add_to_existing_tickets(
                ticket=check_ticket,
                ticket_in=ticket_in,
            )

        ticket = TicketAlchemyModel(
            ticket_name=ticket_in.ticket_name,
            amount=ticket_in.amount,
            acceptor_id=ticket_in.acceptor_id,
            executor_id=self.user.id,
        )
        self.session.add(ticket)
        await self.session.flush()

        await self.message_service.add_message(
            message=ticket_in.message,
            ticket_id=ticket.id,
        )

        if ticket_in.tags_id:
            await validate_tags_in_base(
                tags=ticket_in.tags_id,
                session=self.session,
            )
            associations = [
                TicketTagAssociationAlchemyModel(
                    ticket_id=ticket.id,
                    tag_id=tag,
                )
                for tag in ticket_in.tags_id
            ]
            self.session.add_all(associations)

        await self.session.commit()
        await self.session.refresh(ticket)

        return ticket

    async def ticker_done(
        self,
        ticket_id: int,
    ) -> TicketAlchemyModel | None:

        stmt = select(TicketAlchemyModel.amount).where(
            TicketAlchemyModel.id == ticket_id,
            TicketAlchemyModel.acceptor_id == self.user.id,
        )
        result: Result = await self.session.execute(stmt)
        ticket: int = result.scalar_one_or_none()
        if not ticket:
            return None
        elif ticket <= 1:
            await self.delete_ticket(ticket_id=ticket_id)
            return None

        ticket_done = (
            update(TicketAlchemyModel)
            .where(TicketAlchemyModel.id == ticket_id)
            .values({"amount": ticket - 1})
        )
        await self.session.execute(ticket_done)
        await self.session.commit()
        refresh_ticket: TicketAlchemyModel = await self.session.get(
            TicketAlchemyModel,
            ticket_id,
        )

        return refresh_ticket

    async def add_to_existing_tickets(
        self,
        ticket: TicketAlchemyModel,
        ticket_in: CreateTicket,
    ) -> TicketAlchemyModel:

        self.message_service.add_message(
            message=ticket_in.message,
            ticket_id=ticket.id,
        )

        ticket.amount += ticket_in.amount

        stmt = select(TicketTagAssociationAlchemyModel.tag_id).where(
            TicketTagAssociationAlchemyModel.ticket_id == ticket.id
        )
        result: Result = await self.session.execute(stmt)
        current_tags_ids = set(result.scalars().all())

        if ticket_in.tags_id:
            await validate_tags_in_base(
                tags=ticket_in.tags_id,
                session=self.session,
            )
            new_tags_ids = set(ticket_in.tags_id) - current_tags_ids
            new_tags = [
                TicketTagAssociationAlchemyModel(
                    ticket_id=ticket.id,
                    tag_id=tag,
                )
                for tag in new_tags_ids
            ]
            self.session.add_all(new_tags)

        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def delete_ticket(
        self,
        ticket_id: int,
    ) -> None:
        ticket: TicketAlchemyModel = validate_ticket(
            ticket_id=ticket_id,
            user=self.user,
            session=self.session,
        )
        await self.session.delete(ticket)
        await self.session.commit()

    async def get_ticket(
        self,
        ticket_id: int,
    ) -> TicketAlchemyModel:
        ticket: TicketAlchemyModel = validate_ticket(
            ticket_id=ticket_id,
            user=self.user,
            session=self.session,
        )
        return ticket

# async def update_ticket(ticket_id: int,
#                         ticket_in: UpdateTicket,
#                         executor: UserWithId,
#                         session: AsyncSession) -> TicketAlchemyModel:

#     ticket: TicketAlchemyModel = await validate_ticket(ticket_id=ticket_id,
# user=executor, session=session)

#     if ticket_in.message:
#         await delete_all_messages(ticket_id=ticket_id, user=executor,
# session=session)

#         await add_message(ticket_id=ticket_id,
#                           message=ticket_in.message,
#                           user=executor,
#                           session=session)

#     if ticket_in.amount and ticket_in.amount > ticket.amount:
#         ticket.amount = ticket_in.amount

#     if ticket_in.tags_id:
#         pass
