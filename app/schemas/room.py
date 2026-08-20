from pydantic import BaseModel


class RoomCreate(BaseModel):
    """
    Schema for creating a new room

    Defines the fields required when a client submits
    data to create a new room
    """

    user_id: int
    room_name: str
    floor: str
    room_capacity: int
    is_available: bool
    location_id: int


class RoomResponse(BaseModel):
    """
    Schema for returning Room data in API responses

    """

    id: int
    user_id: int
    room_name: str
    floor: str
    room_capacity: int
    is_available: bool
    location_id: int
