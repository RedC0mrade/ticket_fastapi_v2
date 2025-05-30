from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import UserAlchemyModel
from .base_model import Base


class BlackListAlchemyModel(Base):
    __tablename__ = "black"
    __table_args__ = (UniqueConstraint("user_id", "black_id", name="black_list"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    black_user: Mapped["UserAlchemyModel"] = relationship(
        "UserAlchemyModel",
        back_populates="blacks",
        lazy="selectin",
        foreign_keys=[black_id],
    )

    def __repr__(self) -> str:
        return f"BlackListAlchemyModel(id={self.id!r}, black_id={self.black_id!r})"
