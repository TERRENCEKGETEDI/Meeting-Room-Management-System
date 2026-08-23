from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.schemas.room import RoomCreate, RoomResponse
from app.database.database import SessionLocal
from app.models.room import Room


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

        try:
            # Create a new Room object using the data from the request
            new_room = Room(
                name=room.name,
                floor=room.floor,
                capacity=room.capacity
            )

            
            db.add(new_room)
  
            db.commit()
         
            db.refresh(new_room)

            return new_room

        except IntegrityError:
            
            raise HTTPException(
                status_code=409,
                detail="A room with this name already exists"
            )