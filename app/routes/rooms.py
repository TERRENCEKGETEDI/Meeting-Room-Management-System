"""Delete room route"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.room import Room
from app.schemas.room import RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def list_all_rooms(
    min_capacity: int | None = Query(default=None, gt=0),
    session: Session = Depends(get_db) # noqa: B008
):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        session: Database session used to access the database.
        min_capacity: Optional minimum room capacity
                      It must be greater than 0

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """

    stmt = select(Room)

    if min_capacity is not None:
        stmt = stmt.where(Room.capacity >= min_capacity)

    rooms = session.scalars(stmt).all()

    return rooms


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    session: Session = Depends(get_db)  # noqa: B008
) -> dict[str, str]:
    """
    Delete room function for delete route

    Args:
        room_id: the id of the room
        session: database session

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """

    stmt = select(Room).where(Room.id == room_id)
    room = session.scalars(stmt).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not Found")
    try:
        session.delete(room)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Failed to delete room, room might be linked to other tables, try again",
        )

    return {"message": "Room deleted"}
