
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.security import get_current_user
from app.models.room import Room




def list_all_rooms(
    min_capacity: int | None = Query(default=None, gt=0),
    session: Session = Depends(get_db),  # noqa: B008
    
):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        session: Database session used to access the database.
        min_capacity: Optional minimum room capacity
                      It must be greater than 0
        

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """

    stmt = select(Room)

    if min_capacity is not None:
        stmt = stmt.where(Room.capacity >= min_capacity)

    rooms = session.scalars(stmt).all()

    return rooms