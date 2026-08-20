from fastapi import APIRouter
from app.models.room import Room
from app.database.database import session
from sqlalchemy import select
from app.schemas.room import RoomResponse


room_router = APIRouter(
    prefix="/rooms", tags=["rooms"]
    )

@room_router.get("/",response_model=list[RoomResponse])
def list_all_rooms():
    stmt= select(Room)
    result=session.execute(stmt)
    rooms=result.scalars().all()
    
    return rooms

