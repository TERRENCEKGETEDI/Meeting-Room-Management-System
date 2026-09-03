from fastapi import FastAPI

from app.database.database import Base, engine
from app.routes import rooms, users

app = FastAPI()

# create the tables
Base.metadata.create_all(bind=engine)

# adding the routes 
app.include_router(rooms.router)
app.include_router(users.router)
# ending the routes