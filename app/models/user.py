from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class User(Base):
    """
    Represent Users stored in the database

    Attributes:
        id: Primary Key
        full_name: the full name of the user
        username: the username of the user
        password: the password of the user
        role: the role of the user (admin or user)
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="user"
    )