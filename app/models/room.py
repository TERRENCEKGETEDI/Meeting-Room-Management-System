"""SQLAlchemy model for Room"""

from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, String, ForeignKey


class Room(Base):
    """
    Represent Rooms stored in the database

    Attributes:
        room_id: Primary Key
        user_id: the user who created the id
        room_name: the name of the room
        floor: the floor which the room is
        room_capacity: max number of staff the room can hold
        is_available: confirms if the book is booked/not available or not
        location: where the building is located

        user: a list of rooms can belong to a user (Many-to-One)
        location: a list of rooms can belong to a location (Many-to-One)
    """
    __tablename__ = "room"
    room_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )
    room_name: Mapped[str] = mapped_column(
        String
    )
    floor: Mapped[str] = mapped_column(
        String
    )
    room_capacity: Mapped[int] = mapped_column(
        Integer
    )
    is_available: Mapped[bool] = mapped_column(
        Boolean
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.location_id")
    )

    user: Mapped["Users"] = relationship(
        back_populates="rooms"
    )
    location: Mapped["Location"] = relationship(
        back_populates="rooms"
    )
