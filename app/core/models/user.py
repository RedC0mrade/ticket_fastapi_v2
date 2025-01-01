from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base

class UserAlchemyModel(Base):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(255), unique=True)