from pydantic import BaseModel, ConfigDict


class TicketTagAssociation(BaseModel):
    tag_id: int
    ticket_id: int

    model_config = ConfigDict(from_attributes=True)
