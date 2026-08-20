from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.edit_room import router
from app.routers.list_rooms import list_router
from app.routers.list_by_capacity import list_by_capacity_router

app = FastAPI()

app.include_router(router)
app.include_router(list_router)
app.include_router(list_by_capacity_router)

Base.metadata.create_all(bind=engine)