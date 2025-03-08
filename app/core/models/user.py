import enum
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, LargeBinary, String, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from .base_model import Base


if TYPE_CHECKING:
    from app.core.models.profile import ProfileAlchemyModel
    from app.core.models.ticket import TicketAlchemyModel
    from app.core.models.friend import FriendAlchemyModel
    from app.core.models.follower import FollowerAlchemyModel
    from app.core.models.black_list_user import BlackListAlchemyModel


class UserRoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class UserRoleType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Преобразует Enum в строку при записи в БД"""
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        """Преобразует строку из БД обратно в Enum"""
        if value is None:
            return None
        return UserRoleEnum(value)


class UserAlchemyModel(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileAlchemyModel"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    user_role: Mapped[UserRoleEnum] = mapped_column(
        UserRoleType(),
        default=UserRoleEnum.USER,
        server_default="user",
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
