from fastapi import APIRouter
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomEdit

router = APIRouter(prefix="/edit-room", tags=["Rooms"])


@router.put("/")
def edit_room(room_edit: RoomEdit):
    """
    Edits the the details the room

    Arguments:
    Requires the id of the room you want to edit

    Return:
    returns the rooms details
    """
    with SessionLocal() as session:

        stmt = select(Room).where(Room.id == room_edit.id)
        user_result = session.scalars(stmt).first()

        if user_result is None:
            return {"message": "The id is not found"}

        if room_edit.name is not None:
            user_result.name = room_edit.name
        if room_edit.capacity is not None:
            user_result.capacity = room_edit.capacity
        if room_edit.floor is not None:
            user_result.floor = room_edit.floor

        session.commit()
        session.refresh(user_result)

        return user_result
