from pydantic import BaseModel


class BlackUser(BaseModel):
    user_id: int
    black_id: int
