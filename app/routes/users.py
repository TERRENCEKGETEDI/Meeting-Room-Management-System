from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.users import create_user_service, login_services

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register_user",
             response_model=UserResponse,
             status_code=201
)
def create_user(user: UserCreate,
                session: Session = Depends(get_db)  # noqa: B008
):
    """
    Creates a New user

    Args:
        User = A pydantic schema used to create a user
        session = A database session life cycle

    Return:
        The details of the user
    """
    
    return create_user_service(user,session)


@router.post("/login")
def login(
    user_form: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    session: Session = Depends(get_db)  # noqa: B008
):
    """
    User login route
    Args:
        user_form: OAuth2PasswordRequestForm object containing username and password
        session: database session

    Returns:
        token: access token for the user
    """
    return login_services(user_form, session)
    