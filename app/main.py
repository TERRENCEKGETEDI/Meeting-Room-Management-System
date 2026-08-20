from fastapi import FastAPI

from app.database.database import Base
from app.routes import delete, edit_room
from app.database.database import engine


app = FastAPI()
# create the tables
Base.metadata.create_all(bind=engine)
# adding the routes
app.include_router(delete.router)
app.include_router(edit_room.router)
