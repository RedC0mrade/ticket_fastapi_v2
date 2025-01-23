from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel
from .base_model import Base


class BlackListAlchemyModel(Base):
    __tablename__ = "black"
    __table_args__ = UniqueConstraint("user_id", "black_id", name="black_list")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_user: Mapped["UserAlchemyModel"] = relationship(
        "UserAlchemyModel",
        back_populates="blacks",
        lazy="selectin",
        foreign_keys=[black_id],
    )

    def __repr__(self) -> str:
        return (
            f"BlackListAlchemyModel(id={self.id!r}, "
            f"black_id={self.black_id!r})"
        )
