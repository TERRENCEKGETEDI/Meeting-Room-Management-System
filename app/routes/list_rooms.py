from fastapi import APIRouter,HTTPException
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomResponse

router: APIRouter = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/", response_model=list[RoomResponse])
def list_all_rooms():
    """
    Get a list of all rooms.

    Returns:
        A list of all rooms.
    """
    with SessionLocal() as session:
        stmt = select(Room)
        result = session.execute(stmt)
        rooms = result.scalars().all()
        return rooms
