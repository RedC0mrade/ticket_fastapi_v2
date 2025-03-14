from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel
from .base_model import Base


class FriendAlchemyModel(Base):
    __tablename__ = "friends"
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="unique_friend"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend: Mapped["UserAlchemyModel"] = relationship(
        "UserAlchemyModel",
        back_populates="friends",
        lazy="selectin",
        foreign_keys=[friend_id],
    )

    def __repr__(self) -> str:
        return (
            f"FriendAlchemyModel(id={self.id!r}, friend_id={self.friend_id!r})"
        )
