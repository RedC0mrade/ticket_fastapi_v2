import re
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from app.constant import HEX_COLOR_REGEX


if TYPE_CHECKING:
    from .ticket import TicketAlchemyModel


class TagAlchemyModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(30), unique=True)
    tag_color: Mapped[str] = mapped_column(String(7), unique=True)

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
