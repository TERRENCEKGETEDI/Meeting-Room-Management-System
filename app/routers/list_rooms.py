from fastapi import APIRouter
from app.models.room import Room
from app.database.database import session
from sqlalchemy import select
from app.schemas.room import RoomResponse


list_router = APIRouter(
    prefix="/rooms", tags=["rooms"]
    )

list_router.get("/",response_model=list[RoomResponse])
def list_all_rooms():
    """
        Get a list of the  rooms .
    
        
        Returns:
            A list of the rooms
    """
        
    stmt= select(Room)
    result=session.execute(stmt)
    rooms=result.scalars().all()
    
    return rooms

