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
        floor: the floor in which the room is
        capacity: max number of staff members the room can hold
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
    # A string is a reasonable choice for floor labels because it supports descriptive
    # names such as 'ground' or 'basement', as well as numbers such as '0' or '-1'.
    #
    # If the allowed floors form a fixed set, consider using an enum, as suggested for
    # User.role. This would prevent typos and inconsistent floor labels.
    floor: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    capacity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint( # Good use of a constraint: it enforces positive capacity in the database.
            "capacity>0",
            name="ck_capacity"
        ),
        nullable=False
    )
