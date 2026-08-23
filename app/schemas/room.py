from pydantic import BaseModel, Field


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

class RoomEdit(BaseModel):
    """
    Schema for editing Room details 

    Redefines the fields that the client wants to change

    """
    
    name: str | None = None
    floor: str | None = None
    capacity: int | None =  Field(default=None,gt=0)