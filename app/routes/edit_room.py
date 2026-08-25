from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database.database import SessionLocal
from app.models.room import Room
from app.schemas.room import RoomEdit, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.patch("/{room_id}", response_model=RoomResponse)
def edit_room(room_id: int, room_edit: RoomEdit):
    """
    Edits the the details the room

    Arguments:
        id: Requires the id of the room you want to edit
        room_edit: pydantic schema of the Roomedit controls

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
    # if room_edit.name is not None and room_edit.name.isspace()):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Room name cannot contain a blank space"
    #     )

    if room_edit.capacity is not None and room_edit.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity is less than or equal to 0"
        )

    # Calling using a session object from the main file
    with SessionLocal() as session:

        stmt = select(Room).where(Room.id == room_id)
        user_result = session.scalars(stmt).first()
        # Catches a exception in case the room id ,is not found
        if user_result is None:
            raise HTTPException(
                status_code=404,
                detail="The room id does not exist"
            )
        # if the results collected from the database equals the one's entered display a message
        if (
            user_result.name == room_edit.name
            and user_result.capacity == room_edit.capacity
            and user_result.floor == room_edit.floor
        ):
            raise HTTPException(
                status_code=400,
                detail="No changes made"
            )

        # Name != Null store entered value
        if room_edit.name is not None:
            user_result.name = room_edit.name.strip()

        # Capacity != Null store entered value
        if room_edit.capacity is not None:
            user_result.capacity = room_edit.capacity

        # Floor != Null store entered value
        if room_edit.floor is not None:
            user_result.floor = room_edit.floor.strip()

        try:
            session.commit()
            session.refresh(user_result)
        except (
            IntegrityError
        ):  # Catching a NOtNUllViolation/UniqueViolation and in case of the capacity is 0/zero   to rollback the transaction
            session.rollback()

            raise HTTPException(status_code=409, detail="This room name already exists")

        return user_result
