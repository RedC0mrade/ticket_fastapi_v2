from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel
from .base_model import Base


class FollowerAlchemyModel(Base):
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

    def __repr__(self) -> str:
        return (
            f"FollowerAlchemyModel(id={self.id!r}, "
            f"follower_id={self.follower_id!r})"
            )
