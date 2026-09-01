from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        username: The username of the user being created.
        password: The password of the user being created.
    """

    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for returning user information.

    Attributes:
        id: primary key
        username: The username of the user created.
        password: The password of the user created.
    """

    id: int
    username: str
    role: str
