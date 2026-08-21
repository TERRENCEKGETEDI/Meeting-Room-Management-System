from fastapi import APIRouter
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomResponse

list_by_capacity_router = APIRouter(
    prefix="/list",
    tags=["Rooms"],
)


@list_by_capacity_router.get("/by_capacity/", response_model=list[RoomResponse])
def list_rooms_by_capacity(
    capacity: int
):
    """
    Get a list of rooms filtered by minimum capacity.

    Args:
        capacity: Minimum room capacity to filter by.


    Returns:
        A list of rooms that meet the minimum capacity requirement.
    """

    with SessionLocal() as session:
        stmt = select(Room).where(Room.capacity >= capacity)
        result = session.execute(stmt)
        rooms = result.scalars().all()
        if rooms is None:
            return []
        return rooms
