from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    """
    Schema for creating a new room

    Attributes:
        name: the name of the room
        floor: the floor in which the room is
        capacity: max number of staff the room can hold
    """
    name: str = Field(min_length=1)
    floor: str = Field(min_length=1)
    capacity: int = Field(gt=0)


class RoomResponse(BaseModel):
    """
    Schema for returning Room data in API responses
    Attributes:
        id: Primary Key
        name: the name of the room
        floor: the floor in which the room is
        capacity: max number of staff the room can hold
    """

    id: int
    name: str
    floor: str
    capacity: int


class RoomEdit(BaseModel):
    """
    Schema for editing Room details

    Redefines the fields that the client wants to change

    Attributes:
        name: the name of the room
        floor: the floor in which the room is
        capacity: max number of staff the room can hold
    """
    # Fields are optional for partial updates; if provided, name/floor can't be empty and capacity must be > 0
    name: str | None = Field(default=None, min_length=1)
    floor: str | None = Field(default=None, min_length=1)
    capacity: int | None = Field(default=None, gt=0)
