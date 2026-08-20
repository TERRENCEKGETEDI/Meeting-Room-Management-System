from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.room import Room
from app.database.database import get_db
from app.schemas.room import RoomResponse


list_router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)


@list_router.get("/", response_model=list[RoomResponse])
def list_all_rooms(db: Session = Depends(get_db)):
    """
    Get a list of all rooms.

    Args:
        db (Session): Database session.

    Returns:
        A list of all rooms.
    """

    stmt = select(Room)
    result = db.execute(stmt)
    rooms = result.scalars().all()

    return rooms