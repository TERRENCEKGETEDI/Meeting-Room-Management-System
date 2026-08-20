from sqlalchemy import select

from app.database.database import SessionLocal
from .models.room import Room


with SessionLocal() as session:
    stmt = select(Room)
    room = session.scalars(stmt)
