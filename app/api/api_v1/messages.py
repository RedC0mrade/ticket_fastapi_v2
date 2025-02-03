from fastapi import APIRouter, Depends

from app.core.schemas.message import Message
from app.core.schemas.ticket import Ticket
from app.crud.messages import MessageService
from app.factories.message import get_messages_service


router = APIRouter(tags=["Messages"])


@router.get("/{ticket_id}", response_model=list[Message])
async def get_messages_from_ticket(
    ticket_id: int,
    message_service: MessageService = Depends(get_messages_service),
):

    return await message_service.get_messages(ticket_id=ticket_id)


@router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    message_service: MessageService = Depends(get_messages_service),
):

    return await message_service.delete_message(message_id=message_id)


@router.delete("/all/{ticket_id}", response_model=Ticket)
async def delete_all_messages(
    ticket_id: int,
    message_service: MessageService = Depends(get_messages_service),
):

    return await message_service.delete_all_messages(ticket_id=ticket_id)


@router.post("/", response_model=Message)
async def add_message(
    ticket_id: int,
    message: str,
    message_service: MessageService = Depends(get_messages_service),
):

    return await message_service.add_message(
        ticket_id=ticket_id,
        message=message,
    )


@router.post(
    "/update_message/{message_id}",
    response_model=Message,
)
async def update_message(
    message_id: int,
    message_text: str,
    message_service: MessageService = Depends(get_messages_service),
):

    return await message_service.update_message(
        message_id=message_id,
        message_text=message_text,
    )
