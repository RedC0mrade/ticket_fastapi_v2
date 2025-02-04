from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    id: int
    message: str

    model_config = ConfigDict(from_attributes=True)
