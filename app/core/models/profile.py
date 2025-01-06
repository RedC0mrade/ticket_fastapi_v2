from datetime import date
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base_model import Base
from app.core.models.user import UserAlchemyModel


class ProfileAlchemyModel(Base):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserAlchemyModel"] = relationship(back_populates="profile")
