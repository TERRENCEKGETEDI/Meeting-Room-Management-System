"""SQLAlchemy model for Room"""

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Room(Base):
    """
    Represent Rooms stored in the database

    Attributes:
        id: Primary Key
        name: the name of the room
        floor: the floor which the room is
        capacity: max number of staff the room can hold
        
    """
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    floor: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    capacity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "capacity>0",
            name="ck_capacity"
        ),
        nullable=False
    )
