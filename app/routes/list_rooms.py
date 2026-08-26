from fastapi import APIRouter, Query
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomResponse



router : APIRouter = APIRouter(
    prefix="/rooms",
    tags=["Rooms"] 
    )

@router.get("/", response_model=list[RoomResponse])
def list_all_rooms(min_capacity: int | None = Query(default=None, gt=0)):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        min_capacity: Optional minimum room capacity
                      It must be greater than 0

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """
    with SessionLocal() as session:
        stmt = select(Room)

        if min_capacity is not None:
            stmt = stmt.where(Room.capacity >= min_capacity)

       
        rooms = session.scalars(stmt).all()

        return rooms
