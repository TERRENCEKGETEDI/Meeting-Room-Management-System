from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.room import Room
from app.database.database import SessionLocal
from app.schemas.room import RoomResponse


list_router = APIRouter(
    prefix="/list",
    tags=["Rooms"]
)


@list_router.get("/", response_model=list[RoomResponse])
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
        if rooms is None:
            return []
        return rooms