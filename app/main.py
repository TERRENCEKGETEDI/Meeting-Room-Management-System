from fastapi import FastAPI

from app.database.database import Base, engine
from app.routes import add_room, delete, edit_room, list_by_capacity, list_rooms

app = FastAPI()

# create the tables
Base.metadata.create_all(bind=engine)

# adding the routes 
app.include_router(add_room.router)
app.include_router(delete.router)
app.include_router(edit_room.router)
app.include_router(list_by_capacity.list_by_capacity_router)
app.include_router(list_rooms.list_router)
