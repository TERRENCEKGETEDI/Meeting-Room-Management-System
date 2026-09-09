from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users import create_user_service, login_services

SessionDep = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register_user",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED
             )
def create_user(
    user: UserCreate,
    session: SessionDep
):
    """
    Creates a New user

    Args:
        user: A pydantic schema used to create a user
        session: A database session life cycle

    Return:
        room: The details of the user
    """

    return create_user_service(user, session)


@router.post("/login")
def login(
    user_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db)]
):
    """
    User login route

    Args:
        user_form: OAuth2PasswordRequestForm object
        session: database session

    Returns:
        token: access token for the user
    """
    return login_services(user_form, session)
