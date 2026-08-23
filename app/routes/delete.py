"""Delete room route"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

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
            raise HTTPException(
                status_code=404,
                detail="Room not Found"
            )
        try:
            session.delete(room)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Failed to delete room, room might be linked to other tables, try again"
            )

        return {"message": "Room deleted"}
