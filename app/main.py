from fastapi import FastAPI

from app.database.database import Base, engine
from app.routes import rooms, users

app = FastAPI()


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users.router)
app.include_router(rooms.router)