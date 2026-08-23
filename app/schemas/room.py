from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    """
    Schema for creating a new room

    Defines the fields required when a client submits
    data to create a new room
    """
    name: str = Field(min_length=1)
    floor: Field(min_length=1)
    capacity: Field(gt=0)


class RoomResponse(BaseModel):
    """
    Schema for returning Room data in API responses

    """

    id: int
    name: str
    floor: str
    capacity: int


class RoomEdit(BaseModel):
    """
    Schema for editing Room details

    Redefines the fields that the client wants to change

    """
    # Fields are optional for partial updates; if provided, name/floor can't be empty and capacity must be > 0
    name: str | None = Field(default=None, min_length=1)
    floor: str | None = Field(default=None, min_length=1)
    capacity: int | None = Field(default=None, gt=0)
