from fastapi import APIRouter

from database import SessionLocal
from models.room import Room
from schemas.room import RoomCreate, RoomResponse


# Create a router for room-related endpoints
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post("/", response_model=RoomResponse)
def add_room(room: RoomCreate):
    """
    Create a new meeting room.

    Receives room details from the client, saves the new room
    to the database, and returns the created room.
    """

    # Open a database session
    with SessionLocal() as db:

        # Create a new Room object using the data from the request
        new_room = Room(
            name=room.name,
            floor=room.floor,
            capacity=room.capacity
        )

        # Add the new room to the database session
        db.add(new_room)

        # Save the new room to the database
        db.commit()

        # Refresh the object to get the generated database ID
        db.refresh(new_room)

        # Return the newly created room
        return new_room