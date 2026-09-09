from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomEdit


def list_all_rooms_service(
    session: Session,
    min_capacity: int | None = None,
):
    """
    Get a list of all rooms. Optionally filtered by minimum capacity

    Args:
        session: Database session used to access the database.
        min_capacity: Optional minimum room capacity

    Returns:
        A list of all rooms , filtered by minimum capacity if provided
    """

    stmt = select(Room)

    if min_capacity is not None:
        stmt = stmt.where(Room.capacity >= min_capacity)

    rooms = session.scalars(stmt).all()

    return rooms


def delete_room_service(
        room_id: int,
        session: Session
):
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not Found"
        )
    try:
        session.delete(room)
        session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Failed to delete room, linked to a row"
        )

    return {"message": "Room deleted"}


def add_room_service(room: RoomCreate, session: Session):
    """
        Create a new meeting room.

    Args:
       room:room details
       session: database session
    Returns:
        new_room:The created room
    """
    stripped_name = room.name.strip()
    stripped_floor = room.floor.strip()

    if not stripped_name or not stripped_floor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room name or floor cannot be empty"
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

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A room with this name already exists"
        )


def edit_room_services(room_id: int, room_edit: RoomEdit, session: Session):
    """
    Edits the details of a room.

    Arguments:
        room_id: ID of the room to edit.
        room_edit: Fields to update.
        session: database session

    Return:
        returns the rooms details
    """
    # If the floor, name, and capacity are not entered
    # then return a HTTPException
    if (
        room_edit.floor is None
        and room_edit.name is None
        and room_edit.capacity is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No details provided"
        )

    # Open a database session for the duration of the request.
    stmt = select(Room).where(Room.id == room_id)
    room_result = session.scalars(stmt).first()
    # Catches a exception in case the room id ,is not found
    if room_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The room id does not exist"
        )

    # App;y only the fields that were provided.
    for field, value in room_edit.model_dump(exclude_unset=True).items():
        setattr(room_result, field, value)

    # Check whether the values actually changed
    if not session.is_modified(room_result):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No changes made"
        )

    session.commit()
    session.refresh(room_result)

    return room_result
