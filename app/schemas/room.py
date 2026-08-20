from pydantic import BaseModel


class RoomDelete(BaseModel):
    """
    Schema for deleting a room

    Attributes:
        id: recieved
    """

    id: int


class RoomCreate(BaseModel):
    """
    Schema for creating a new room

    Defines the fields required when a client submits
    data to create a new room
    """

    name: str
    floor: str
    capacity: int


class RoomResponse(BaseModel):
    """
    Schema for returning Room data in API responses

    """

    id: int
    name: str
    floor: str
    capacity: int
