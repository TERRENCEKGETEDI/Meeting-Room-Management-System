from fastapi import APIRouter, Query ,  HTTPException
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomResponse

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.get("/list", response_model=list[RoomResponse])
def list_rooms_by_capacity(
    min_capacity: int = Query(gt=0)
):
    """
    Get a list of rooms filtered by minimum capacity.

    Args:
        min_capacity: Minimum room capacity to filter by.
        It must be an integer and it must be greater than 0."

    Returns:
        A list of rooms that meet the minimum capacity requirement.
    """

    with SessionLocal() as session:
        stmt = select(Room).where(Room.capacity >= min_capacity)
        result = session.execute(stmt)
        rooms = result.scalars().all()
        
        
        if not rooms:
            raise HTTPException(
                status_code=404,
                detail="No rooms found with the requested capacity"
            )

        return rooms
