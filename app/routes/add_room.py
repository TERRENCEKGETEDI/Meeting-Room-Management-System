from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.schemas.room import RoomCreate, RoomResponse
from app.database.database import SessionLocal
from app.models.room import Room


# Create a router for room-related endpoints
router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=201
)
def add_room(room: RoomCreate):
    """
    Create a new meeting room.

    Receives room details, saves the room to the database,
    and returns the created room.
    """
    # Remove leading and trailing whitespace
    stripped_name = room.name.strip()
    stripped_floor = room.floor.strip()

    if not stripped_name or not stripped_floor:
        raise HTTPException(
            status_code=400,
            detail="Room name and floor cannot be empty"
        )

    with SessionLocal() as db:
        try:
            new_room = Room(
                name= stripped_name,
                floor = stripped_floor,
                capacity=room.capacity
            )

            db.add(new_room)
            db.commit()
            db.refresh(new_room)

            return new_room

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=409,
                detail="A room with this name already exists"
            )