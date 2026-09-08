from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.room import Room


def delete_room_service(
    room_id: int,
    session: Session
):
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not Found")
    try:
        session.delete(room)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to delete room, room might be linked to other tables, try again",
        )

    return {"message": "Room deleted"}