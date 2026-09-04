from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    # full_name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    # role: str = Field(min_length=1)


# class UserLogin(BaseModel):
#     # full_name: str = Field(min_length=1)
#     username: str = Field(min_length=1)
#     password: str = Field(min_length=1)
#     # role: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: int
    # full_name: str
    username: str
    # role: str


class UserEdit(BaseModel):
    # full_name: str | None = Field(default=None, min_length=1)
    username: str | None = Field(default=None, min_length=1)
    password: str | None = Field(default=None, min_length=1)
    # role: str | None = Field(default=None, min_length=1)
