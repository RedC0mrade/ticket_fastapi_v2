from sqlalchemy import ForeignKey, UniqueConstraint
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel


class FriendAlchemyModel(BaseModel):
    __tablename__ = "friends"
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="unique_friend"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend: Mapped["UserAlchemyModel"] = relationship(
        "UserAlchemyModel",
        back_populates="frends",
        lazy="selectin",
    )
