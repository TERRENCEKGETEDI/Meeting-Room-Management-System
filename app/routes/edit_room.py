from fastapi import APIRouter
from app.models.room import Room
from app.schemas.room import RoomEdit
from app.database import database
from sqlalchemy import select

router = APIRouter(
    prefix="/edit-room",
    tags=["Rooms"]
)

@router.put("/{id}")
def edit_room(room_edit: RoomEdit):

    """
     Edits the the details the room 

     Arguments: 
     Requires the id of the room you want to edit

     Return: 
     returns the rooms details
    """
    session = database.SessionLocal()

    stmt= select(Room).where(Room.id == room_edit.id)
    user_result =  session.scalars(stmt).first()

    if user_result is None:
        return {"":"not"}

    if room_edit.name is not None:
        user_result.name=room_edit.name
    if room_edit.capacity is not None:
        user_result.capacity=room_edit.capacity
    if room_edit.floor is not None:
            user_result.floor=room_edit.floor
            
    session.commit()
    session.refresh(user_result)

    return user_result

    

   

            