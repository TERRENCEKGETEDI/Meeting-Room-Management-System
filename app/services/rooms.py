
from fastapi import HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomEdit


def list_all_rooms_service(
    session: Session,
    # Please change this parameter to `min_capacity: int | None = None`. Keep Query
    # metadata in the route or its FastAPI dependencies, where it describes and validates
    # HTTP query parameters. This service is called as an ordinary Python function:
    # omitting the argument would pass a Query object here, rather than None. Using None
    # makes the default behave correctly and keeps the service independent of HTTP input.
    min_capacity: int | None = Query(default=None, gt=0),
    
    
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

def add_room_service(
    room: RoomCreate,
    session: Session
):
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
            status_code=400, detail="Room name or floor cannot be empty"
        )

    try:
        new_room = Room(
            name=stripped_name, 
            floor=stripped_floor, 
            capacity=room.capacity
        )

        session.add(new_room)
        session.commit()
        session.refresh(new_room)

        return new_room

    except IntegrityError:
        # Please remove this explicit rollback. The following raise ends this operation,
        # so the session is no longer used after the error. The get_db() dependency closes
        # the session during cleanup and releases its transaction resources. Each request
        # receives a new session, so other requests are unaffected.
        #
        # An explicit rollback is needed after a failed flush if the same session will
        # continue to be used. That is not the case here, so restoring it to a usable
        # state before closing it adds unnecessary cleanup code.
        #
        # Apply this change wherever the session is no longer used after an error and
        # is closed by the dependency. Keep rollbacks where that session is reused.
        session.rollback()

        # Please use constants from FastAPI's status module for HTTP status codes
        # throughout the codebase. For example, status.HTTP_409_CONFLICT makes the
        # response's meaning clear without requiring the reader to remember what 409
        # means. This is a readability and consistency improvement. See:
        # https://fastapi.tiangolo.com/reference/status/
        raise HTTPException(
            status_code=409, 
            detail="A room with this name already exists"
        )

def edit_room_services(
    room_id: int,
    room_edit: RoomEdit,
    session: Session 
):
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

    # Open a database session for the duration of the request.
    stmt = select(Room).where(Room.id == room_id)
    room_result = session.scalars(stmt).first()
    # Catches a exception in case the room id ,is not found
    if room_result is None:
        raise HTTPException(status_code=404, detail="The room id does not exist")

    # The original update logic had well-considered checks, but repeated similar code
    # for each field. I have replaced it below with a Pydantic model_dump() loop and
    # SQLAlchemy's is_modified() check. The loop applies non-None values, and
    # is_modified() detects whether the stored values would actually change. This
    # removes the need to maintain a separate changes_made flag for every field.
    # Please complete this approach by adding the schema validation described below.

    for field, value in room_edit.model_dump(exclude_none=True).items():
        # This requires the Pydantic field names to match the SQLAlchemy attribute names.
        setattr(room_result, field, value)

    if not session.is_modified(room_result):
        raise HTTPException(status_code=400, detail="No changes made")

    # Please configure RoomEdit to strip leading and trailing whitespace and reject
    # strings that are empty after stripping. The update loop above does not perform
    # those checks, so this schema change is needed to prevent blank names and floors:
    #
    #   class RoomEdit(BaseModel):
    #       model_config = ConfigDict(str_strip_whitespace=True)
    #
    #       name: str | None = Field(default=None, min_length=1)
    #       floor: str | None = Field(default=None, min_length=1)
    #       capacity: int | None = Field(default=None, gt=0)
    #
    # Import ConfigDict from pydantic for this example. str_strip_whitespace applies to
    # all string fields in the model; it does not affect capacity. Stripping happens
    # before the minimum-length check, so strings containing only whitespace are
    # rejected. Use field-specific validation if some strings must be preserved.
    # I have removed the manual isspace() checks in anticipation of this schema change.
    # The manual capacity check is also removed because RoomEdit already enforces
    # capacity > 0 through its field constraint.
    #
    # FastAPI validates the request body with this model before calling the route
    # function, so invalid input is rejected before reaching the service. Validation
    # errors produce a 422 response by default, rather than the previous manual 400.
    # Apply the same whitespace handling to RoomCreate, then remove the duplicate
    # stripping and empty-string checks in add_room_service(). Check for other suitable
    # places to move input validation into schemas so each rule has one clear home.

    try:
        session.commit()
        session.refresh(room_result)
    except (
        IntegrityError
    ):  # Catching a NOtNUllViolation/UniqueViolation  to rollback the transaction
        session.rollback()

        raise HTTPException(status_code=409, detail="This room name already exists")

    return room_result
