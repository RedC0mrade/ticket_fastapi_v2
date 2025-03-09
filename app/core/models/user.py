from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from .base_model import Base


if TYPE_CHECKING:
    from app.core.models.profile import ProfileAlchemyModel
    from app.core.models.ticket import TicketAlchemyModel
    from app.core.models.friend import FriendAlchemyModel
    from app.core.models.follower import FollowerAlchemyModel
    from app.core.models.black_list_user import BlackListAlchemyModel


class UserAlchemyModel(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    # password: Mapped[str] = mapped_column(String(255), nullable=False)
    # email: Mapped[str] = mapped_column(String(255), unique=True)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileAlchemyModel"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    friends: Mapped[list["FriendAlchemyModel"]] = relationship(
        back_populates="friend",
        foreign_keys="[FriendAlchemyModel.friend_id]",
        cascade="all, delete-orphan",
    )
    followers: Mapped[list["FollowerAlchemyModel"]] = relationship(
        back_populates="follower",
        foreign_keys="[FollowerAlchemyModel.follower_id]",
        cascade="all, delete-orphan",
    )
    fans: Mapped[list["FollowerAlchemyModel"]] = relationship(
        back_populates="fan",
        foreign_keys="[FollowerAlchemyModel.user_id]",
        cascade="all, delete-orphan",
    )
    blacks: Mapped[list["BlackListAlchemyModel"]] = relationship(
        back_populates="black_user",
        foreign_keys="[BlackListAlchemyModel.black_id]",
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
