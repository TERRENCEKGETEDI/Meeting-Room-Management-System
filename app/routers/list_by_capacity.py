from fastapi import APIRouter
from app.models.room import Room
from app.database.database import session
from sqlalchemy import select
from app.schemas.room import RoomResponse


list_by_capacity_router = APIRouter(
    prefix="/rooms", tags=["rooms"]
    )

@list_by_capacity_router.get("/",response_model=list[RoomResponse])
def list_rooms_by_capacity(capacity: int):
    """
    Get a list of rooms filtered by minimum capacity.

    Args:
        capacity (int): Minimum room capacity to filter by.

    Returns:
        A list of rooms that meet the minimum capacity requirement.
    """
    
    stmt= select(Room).where(Room.capacity >=capacity)
    result=session.execute(stmt)
    rooms=result.scalars().all()
    
    return rooms