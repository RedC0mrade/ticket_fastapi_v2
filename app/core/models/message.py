from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


if TYPE_CHECKING:
    from .ticket import TicketAlchemyModel


class MessageAlchemyModel(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(250), nullable=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    ticket: Mapped["TicketAlchemyModel"] = relationship(
        "TicketAlchemyModel", back_populates="messages"
    )

    def __repr__(self) -> str:
        return f"MessageAlchemyModel(id={self.id!r}, message={self.message!r})"
