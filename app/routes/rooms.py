"""room routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.security import get_current_user, require_admin
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomEdit, RoomResponse
from app.services.rooms import (
    add_room_service,
    delete_room_service,
    list_all_rooms_service,
    edit_room_services
)

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def list_all_rooms(
    min_capacity: int | None = Query(default=None, gt=0),
    session: Session = Depends(get_db),  # noqa: B008
    current_user: str = Depends(get_current_user),
):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        session: Database session used to access the database.
        min_capacity: Optional minimum room capacity
                      It must be greater than 0
        current_user: current user for authorization
        

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """

    return list_all_rooms_service(session,min_capacity,)


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    session: Session = Depends(get_db),  # noqa: B008
    current_user: str = Depends(require_admin),
) -> dict[str, str]:
    """
    Delete room function for delete route

    Args:
        room_id: the id of the room
        session: database session
        current_user: the current user making the request

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """
    return delete_room_service(room_id, session)


@router.patch("/{room_id}", response_model=RoomResponse)
def edit_room(
    room_id: int,
    room_edit: RoomEdit,
    session: Session = Depends(get_db),  # noqa: B008
    current_user: str = Depends(require_admin),
):
    """
    Edits the details of a room.

    Arguments:
        room_id: ID of the room to edit.
        room_edit: Fields to update.
        session: database session
        current_user: the current user making the request

    Return:
        returns the rooms details
    """
    

    return edit_room_services(room_id,room_edit,session)


@router.post("/", response_model=RoomResponse,
              status_code=201)
def add_room(
    room: RoomCreate,
    session: Session = Depends(get_db),  # noqa: B008
    current_user: str = Depends(require_admin),
):
    """
        Create a new meeting room.

    Args:
       room: room details
        session: database session
        current_user: the current user making the request
    Returns:
        new_room:The created room
    """
    return add_room_service(room, session)
