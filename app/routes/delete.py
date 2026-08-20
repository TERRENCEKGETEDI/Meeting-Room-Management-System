"""Delete route"""

from sqlalchemy import select

from fastapi import APIRouter

from app.database.database import SessionLocal
from app.models.room import Room


router = APIRouter(prefix="/users", tags=["Users"])


@router.delete("/{id}")
def delete_room(
    id: int
) -> dict[str, str]:
    """
    Delete room route

    Args:
        id: the id of the room
        session: the database session
    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """
    session = SessionLocal()
    stmt = select(Room).where(
        Room.id == id
    )
    room = session.scalars(stmt).first()
    if room is None:
        return {"message": "Room not found"}

    session.delete(room)
    session.commit()

    return {"message": "Room deleted"}
