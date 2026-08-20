from fastapi import FastAPI
from app.routes import edit_room
from app.database.database import Base, engine
from app.routes.edit_room import router
from app.routes.list_rooms import list_router
from app.routes.list_by_capacity import list_by_capacity_router

app = FastAPI()

app.include_router(edit_room.router)
app.include_router(router)
app.include_router(list_router)
app.include_router(list_by_capacity_router)
Base.metadata.create_all(bind=engine)