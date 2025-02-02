from typing import Annotated, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.schemas.tag import Tag
from app.core.schemas.user import UserBase
from app.core.schemas.message import Message


PositiveInt = Annotated[int, Field(gt=0)]


class Ticket(BaseModel):
    id: int
    ticket_name: str
    messages: Optional[List[Message]] = None
    tags: List[Tag]
    amount: int
    acceptor: UserBase
    executor: UserBase

    model_config = ConfigDict(from_attributes=True)


class CreateTicket(BaseModel):
    ticket_name: str
    message: str
    amount: PositiveInt
    acceptor_id: PositiveInt
    tags_id: list[PositiveInt]


class UpdateTicket(BaseModel):
    message: str | None = None
    amount: PositiveInt | None = None
    tags_id: list[PositiveInt] | None = None
