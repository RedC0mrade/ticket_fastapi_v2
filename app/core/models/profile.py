from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base_model import Base
from app.core.models.user import UserAlchemyModel


class ProfileAlchemyModel(Base):
    __tablename__ = "profiles"

    name: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[date]
    user: Mapped["UserAlchemyModel"] = relationship(back_populates="profile")
