from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomEdit

router = APIRouter(prefix="/room", tags=["Rooms"])

@router.put("/{room_id}")
def edit_room(room_id: int,room_edit: RoomEdit):
    """
    Edits the the details the room

    Arguments:
    Requires the id of the room you want to edit

    Return:
    returns the rooms details
    """
    if room_edit.floor is None and room_edit.name is None and room_edit.capacity is None:
       raise HTTPException(
           status_code=400,
           detail="No details provdided"
       )

    with SessionLocal() as session:

        stmt = select(Room).where(Room.id == room_id)
        user_result = session.scalars(stmt).first()

        if user_result is None:
           raise HTTPException(
               status_code=404,
               detail="The room id does not exist"
           )
        
        if user_result.name == room_edit.name and user_result.capacity == room_edit.capacity and user_result.floor == room_edit.floor:
            return{"message":"no changes made"}
        
        if room_edit.name is not None:
            user_result.name = room_edit.name
        if room_edit.capacity is not None:
            user_result.capacity = room_edit.capacity
        if room_edit.floor is not None:
            user_result.floor = room_edit.floor

        try:
            session.commit()
            session.refresh(user_result)
        except IntegrityError:
            session.rollback()

            raise HTTPException(
                status_code=400,
                detail="Could not update the room"
            )

        return user_result