from typing import TYPE_CHECKING
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


if TYPE_CHECKING:
    from .profile import ProfileAlchemyModel
    from .ticket import TicketAlchemyModel


class UserAlchemyModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    profile: Mapped["ProfileAlchemyModel"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    to_do_tickets: Mapped[list["TicketAlchemyModel"]] = relationship(
        "TicketAlchemyModel",
        foreign_keys="[TicketAlchemyModel.executor_id]",
        back_populates="executor",
        cascade="all, delete-orphan",
    )

    to_take_tickets: Mapped[list["TicketAlchemyModel"]] = relationship(
        "TicketAlchemyModel",
        foreign_keys="[TicketAlchemyModel.acceptor_id]",
        back_populates="acceptor",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"UserAlchemyModel(id={self.id!r}, username={self.username!r})"
