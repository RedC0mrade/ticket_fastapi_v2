from typing import List
from fastapi import APIRouter, Depends

from app.core.schemas.ticket import Ticket, CreateTicket
from app.crud.tickets import TicketService
from app.factories.ticket import get_ticket_service


router = APIRouter(tags=["ticket"])


@router.post("/", response_model=Ticket, status_code=201)
async def create_ticket(
    ticket_in: CreateTicket,
    ticket_service: TicketService = Depends(get_ticket_service),
):
    return await ticket_service.create_ticket(ticket_in=ticket_in)


@router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(
    ticket_id: int,
    ticket_service: TicketService = Depends(get_ticket_service),
):

    return await ticket_service.delete_ticket(ticket_id=ticket_id)


@router.get("/my_tickets", response_model=List[Ticket])
async def get_my_tickets(
    ticket_service: TicketService = Depends(get_ticket_service),
):
    return await ticket_service.get_my_tickets()


@router.get("/my_tasks", response_model=List[Ticket])
async def get_my_tasks(
    ticket_service: TicketService = Depends(get_ticket_service),
):
    return await ticket_service.get_my_tasks()


@router.post("/ticket_done/{ticked_id}", response_model=Ticket | None)
async def ticket_done(
    ticket_id: int,
    ticket_service: TicketService = Depends(get_ticket_service),
):

    return await ticket_service.ticker_done(ticket_id)


@router.post("/add_to_existing_ticket/{ticked_id}", response_model=Ticket)
async def add_to_existing_tickets(
    ticket_id: int,
    amount: int,
    message: str,
    ticket_service: TicketService = Depends(get_ticket_service),
):

    return await ticket_service.add_to_existing_tickets(
        ticket_id=ticket_id,
        amount=amount,
        message=message,
    )


@router.get("/ticket", response_model=Ticket)
async def get_ticket(
    ticket_id: int,
    ticket_service: TicketService = Depends(get_ticket_service),
):
    return await ticket_service.get_ticket(ticket_id=ticket_id)


# @router.get("/update_ticket/{ticket_id}", response_model=Ticket)
# async def update_ticket(
#     ticket_in: UpdateTicket,
#     ticket_id: int,
#     ticket_service: TicketService = Depends(get_ticket_service),
# ):
#     return await ticket_service.update_ticket(
#         ticket_id=ticket_id,
#         ticket_in=ticket_in,
#     )
