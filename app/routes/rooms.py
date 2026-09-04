""""Room routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_current_user, require_admin
from app.database.dependencies import get_db
from app.models.users import User
from app.schemas.room import RoomCreate, RoomEdit, RoomResponse
from app.services.rooms import (
    add_room_services,
    delete_room_services,
    edit_room_services,
    list_all_rooms_services,
)

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=201)
def add_room(
    room: RoomCreate,
    current_user: User = Depends(require_admin),  # noqa: B008
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
        Create a new meeting room.

    Args:
       room: room details
       current_user: The user making the request (must be an admin)
       session: AsyncSession for database interaction
    Returns:
        new_room: The created room
    """
    return add_room_services(room, session)


@router.delete("/{room_id}")
async def delete_room(
    room_id: int,
    current_user: User = Depends(require_admin),  # noqa: B008
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
    Delete room function for delete route

    Args:
        room_id: the id of the room
        current_user: The user making the request (must be an admin)
        session: AsyncSession for database interaction

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """
    return await delete_room_services(room_id, session)


@router.patch("/{room_id}", response_model=RoomResponse)
def edit_room(
    room_id: int,
    room_edit: RoomEdit,
    current_user: User = Depends(require_admin),  # noqa: B008
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
    Edits the details of a room.

    Args:
        room_id: ID of the room to edit.
        room_edit: Fields to update.
        current_user: The user making the request (must be an admin)
        session: AsyncSession for database interaction

    Returns:
        room: The updated room details
    """
    return edit_room_services(room_id, room_edit, session)


@router.get("/", response_model=list[RoomResponse])
def list_all_rooms(
    min_capacity: int | None = Query(default=None, gt=0),
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        min_capacity: Optional minimum capacity to filter rooms
        current_user: The user making the request
        session: AsyncSession for database interaction

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """
    return list_all_rooms_services(session, min_capacity)
