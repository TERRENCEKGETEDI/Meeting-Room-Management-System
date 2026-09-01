from pydantic import Basemodel

class UserCreate(Basemodel):
    """
    Schema for creating a new user.

    Defines the information required when a client
    submits data to create a user.
    """
    username: str
    password: str

class UserResponse(Basemodel):
    """Schema for returning user information.

    The password is not included in the response."""
    id: int
    username: str
    role: str


