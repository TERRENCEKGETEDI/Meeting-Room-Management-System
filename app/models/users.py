"""SQLAlchemy model for Room"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.auth.roles import UserRole
from app.database.database import Base


class User(Base):
    """
    Represent Users stored in the database

    Attributes:
        id: Primary Key
        full_name: the name of the user
        username: unique name of the user
        password: password of the user
        role: role of the user
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    # full_name: Mapped[str] = mapped_column(
    #     String,
    #     unique=True,
    #     nullable=False
    # )
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
        default=UserRole.USER.value,
        nullable=False
    )
