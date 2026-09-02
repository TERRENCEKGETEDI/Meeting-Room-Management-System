"""Delete room route"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.room import Room
from app.schemas.room import RoomEdit, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    session: Session = Depends(get_db)  # noqa: B008
) -> dict[str, str]:
    """
    Delete room function for delete route

    Args:
        room_id: the id of the room
        session: database session

    Returns:
        message: Room deleted or Room not found if room doesn't exist
    """
    
    stmt = select(Room).where(
        Room.id == room_id
    )
    room = session.scalars(stmt).first()
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not Found"
        )
    try:
        session.delete(room)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Failed to delete room, room might be linked to other tables, try again"
        )

    return {"message": "Room deleted"}

@router.patch("/{room_id}", response_model=RoomResponse)
def edit_room(room_id: int, 
              room_edit: RoomEdit,
              session: Session = Depends(get_db)
):
    """
    Edits the details of a room.

    Arguments:
        room_id: ID of the room to edit.
        room_edit: Fields to update.

    Return:
        returns the rooms details
    """
    # If the floor, name, and capacity are not entered than return a HTTPException
    if (
        room_edit.floor is None
        and room_edit.name is None
        and room_edit.capacity is None
    ):
        raise HTTPException(status_code=400, detail="No details provdided")

    # if invalid values were provided
    if ((room_edit.floor is not None and room_edit.floor.isspace()) or
            (room_edit.name is not None and room_edit.name.isspace())):
        raise HTTPException(
            status_code=400,
            detail="Floor OR Name cannot contain a blank space"
        )

    if room_edit.capacity is not None and room_edit.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity is less than or equal to 0"
        )

    # Open a database session for the duration of the request.

    stmt = select(Room).where(Room.id == room_id)
    room_result = session.scalars(stmt).first()
    # Catches a exception in case the room id ,is not found
    if room_result is None:
        raise HTTPException(
            status_code=404,
            detail="The room id does not exist"
        )
    
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
            raise HTTPException(
                status_code=400,
                detail="No changes made"
            )    
        
    try:
        session.commit()
        session.refresh(room_result)
    except IntegrityError:  # Catching a NOtNUllViolation/UniqueViolation  to rollback the transaction
        session.rollback()

        raise HTTPException(status_code=409, detail="This room name already exists")

    return room_result

