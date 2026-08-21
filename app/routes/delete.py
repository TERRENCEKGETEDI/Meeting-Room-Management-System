"""Delete room route"""

from fastapi import APIRouter
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room

router = APIRouter(prefix="/room", tags=["Rooms"])


@router.delete("/{room_id}")
def delete_room(
    room_id: int
) -> dict[str, str]:
    """
    Delete room route

    Args:
        room_id: the id of the room

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """
    with SessionLocal() as session:
        stmt = select(Room).where(
            Room.id == room_id
        )
        room = session.scalars(stmt).first()
        if room is None:
            return {"message": "Room not found"}

        session.delete(room)
        session.commit()

        return {"message": "Room deleted"}
