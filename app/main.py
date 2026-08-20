from fastapi import FastAPI

from app.database.database import Base
from app.routes import delete
from app.database.database import engine


app = FastAPI()

# create the tables
Base.metadata.create_all(bind=engine)

# adding the routes
app.include_router(delete.router)
