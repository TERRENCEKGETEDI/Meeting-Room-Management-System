from fastapi import APIRouter
from app.models.room import Room
from app.database.database import session
from sqlalchemy import select
from app.schemas.room import RoomResponse


room_router = APIRouter(
    prefix="/rooms", tags=["rooms"]
    )

@room_router.get("/",response_model=list[RoomResponse])
def list_rooms_by_capacity(capacity:int, room):
    stmt= select(Room).where(Room.capacity >=capacity)
    result=session.execute(stmt)
    rooms=result.scalars().all()
    
    return rooms