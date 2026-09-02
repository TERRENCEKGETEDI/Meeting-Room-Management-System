"""room routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomEdit, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
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


@router.delete("/{room_id}")
def delete_room(room_id: int, session: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete room function for delete route

    Args:
        room_id: the id of the room
        session: database session

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """

    stmt = select(Room).where(Room.id == room_id)
    room = session.scalars(stmt).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not Found")
    try:
        session.delete(room)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Failed to delete room, room might be linked to other tables, try again",
        )

    return {"message": "Room deleted"}


@router.patch("/{room_id}", response_model=RoomResponse)
def edit_room(room_id: int, room_edit: RoomEdit, session: Session = Depends(get_db)):
    """
    Edits the details of a room.

    Arguments:
        room_id: ID of the room to edit.
        room_edit: Fields to update.
        session: database session

    Return:
        returns the rooms details
    """
    # If the floor, name, and capacity are not entered than return a HTTPException
    if (
        room_edit.floor is None
        and room_edit.name is None
        and room_edit.capacity is None
    ):
        raise HTTPException(status_code=400, detail="No details provided")

    # if invalid values were provided
    if (room_edit.floor is not None and room_edit.floor.isspace()) or (
        room_edit.name is not None and room_edit.name.isspace()
    ):
        raise HTTPException(
            status_code=400, detail="Floor OR Name cannot contain a blank space"
        )

    if room_edit.capacity is not None and room_edit.capacity <= 0:
        raise HTTPException(
            status_code=400, detail="Capacity is less than or equal to 0"
        )

    # Open a database session for the duration of the request.
    stmt = select(Room).where(Room.id == room_id)
    room_result = session.scalars(stmt).first()
    # Catches a exception in case the room id ,is not found
    if room_result is None:
        raise HTTPException(status_code=404, detail="The room id does not exist")

    changes_made = False

    # Update the room name only when a new name was provided.
    if room_edit.name is not None:
        new_name = room_edit.name.strip()
        # Checks if changes were made
        if new_name != room_result.name:
            room_result.name = new_name
            changes_made = True

    # Update the room capacity only when a new name was provided.
    if room_edit.capacity is not None:
        if room_edit.capacity != room_result.capacity:
            room_result.capacity = room_edit.capacity
            changes_made = True

    # Update the room floor only when a new name was provided.
    if room_edit.floor is not None:
        new_floor = room_edit.floor.strip()

        if new_floor != room_result.floor:
            room_result.floor = new_floor
            changes_made = True

    if not changes_made:
        raise HTTPException(status_code=400, detail="No changes made")

    try:
        session.commit()
        session.refresh(room_result)
    except (
        IntegrityError
    ):  # Catching a NOtNUllViolation/UniqueViolation  to rollback the transaction
        session.rollback()

        raise HTTPException(status_code=409, detail="This room name already exists")

    return room_result


@router.post("/", response_model=RoomResponse, status_code=201)
def add_room(room: RoomCreate, session: Session = Depends(get_db)):
    """
        Create a new meeting room.

    Args:
       room: room details
    Returns:
        new_room:The created room
    """
    stripped_name = room.name.strip()
    stripped_floor = room.floor.strip()

    if not stripped_name or not stripped_floor:
        raise HTTPException(
            status_code=400, detail="Room name or floor cannot be empty"
        )

    try:
        new_room = Room(
            name=stripped_name, floor=stripped_floor, capacity=room.capacity
        )

        session.add(new_room)
        session.commit()
        session.refresh(new_room)

        return new_room

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409, detail="A room with this name already exists"
        )
