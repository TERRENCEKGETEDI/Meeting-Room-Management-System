from fastapi import FastAPI
from app.routes import edit_room
from app.database.database import Base, engine

app = FastAPI()

app.include_router(edit_room.router)

Base.metadata.create_all(bind=engine)