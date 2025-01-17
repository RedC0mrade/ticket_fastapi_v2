from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class TicketTagAssociationAlchemyModel(Base):
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
