from sqlalchemy import ForeignKey, UniqueConstraint
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel


class FollowerAlchemyModel(BaseModel):
    __tablename__ = "followers"
    __table_args__ = (
        UniqueConstraint("user_id", "follower_id", name="unique_follower"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    follower: Mapped["UserAlchemyModel"] = relationship(
        "UserAlchemyModel",
        back_populates="followers",
        lazy="selectin",
    )
