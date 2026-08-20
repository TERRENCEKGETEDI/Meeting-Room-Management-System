from sqlalchemy import select
from fastapi import FastAPI
from app.database.database import SessionLocal
from app.models.room import Room
from app.routers.list_rooms import list_router
from app.routers.list_by_capacity import list_by_capacity_router


with SessionLocal() as session:
    stmt = select(Room)
    room = session.scalars(stmt)
    
app = FastAPI()  



app.include_router(list_router)
app.include_router(list_by_capacity_router)
