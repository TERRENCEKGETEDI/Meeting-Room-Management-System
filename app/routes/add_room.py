from fastapi import APIRouter

from database import SessionLocal
from models.room import Room
from schemas.room import RoomCreate, RoomResponse


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

    db = SessionLocal()

    try:
        new_room = Room(
            name=room.name,
            floor=room.floor,
            capacity=room.capacity
        )

        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        return new_room

    finally:
        db.close()