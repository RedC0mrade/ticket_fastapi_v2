import re
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from app.constant import HEX_COLOR_REGEX


if TYPE_CHECKING:
    from .ticket import TicketAlchemyModel


class TagAlchemyModel(Base):
    __tablename__ = "tags"

    tag_name: Mapped[str] = mapped_column(String(30))
    tag_color: Mapped[str] = mapped_column(String(7))

    tickets: Mapped[list["TicketAlchemyModel"]] = relationship(
        secondary="ticket_tag", back_populates="tags"
    )

    def __init__(self, tag_color: str, tag_name: str):
        if not re.match(HEX_COLOR_REGEX, tag_color):
            raise ValueError(f"invalid color format {tag_color}")
        self.tag_color = tag_color
        self.tag_name = tag_name

    def __repr__(self) -> str:
        return f"Tag(id={self.id}, tag_name={self.tag_name})"


class TicketTagAssociation(Base):
    __tablename__ = "ticket_tag"
    __table_args__ = (
        UniqueConstraint("ticket_id", "tag_id", name="unique_tag_ticket"),
    )

    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    def __repr__(self) -> str:
        return (
            f"Association("
            f"id={self.id}, "
            f"Association_id={self.ticket_id}, "
            f"Association_id={self.tag_id}"
            f")"
        )
