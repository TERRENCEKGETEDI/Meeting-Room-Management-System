from fastapi import FastAPI
from app.routes import delete
from app.routes import edit_room
from app.database.database import Base, engine

app = FastAPI()

# create the tables
Base.metadata.create_all(bind=engine)

# adding the routes
app.include_router(delete.router)
app.include_router(edit_room.router)