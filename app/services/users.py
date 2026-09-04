from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.dependencies.database import get_db
from app.dependencies.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


def login_services(
    user_form: OAuth2PasswordRequestForm,
    session: Session
):
    """
    User login route

    Args:
        user_form: OAuth2PasswordRequestForm object containing username and password
        session: database session 

    Returns:
        token: access token for the user
    """
    stmt = select(User).where(
        User.username == user_form.username
    )
    existing_user = session.scalar(stmt)

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    if not verify_password(
        user_form.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    token = create_access_token(existing_user.username)

    return {
            "access_token": token,
            "token_type": "bearer"
        }
    
def create_user_service(
    user: UserCreate,
    session: Session
):
    """
    Creates a New user

    Args:
        user  = A pydantic schema used to create a user
        session = A database session life cycle

    Return:
        The details of the user
    """
    stripped_fullname = user.full_name.strip()
    stripped_username = user.username.strip()
    stripped_password = user.password.strip()

    if not stripped_username or not stripped_password or not stripped_fullname:
        raise HTTPException(
            status_code=400,
            detail="Fullname or Username or password cannot be empty"
        )

    hashed_password = hash_password(stripped_password)

    new_user = User(
        full_name=stripped_fullname,
        username=stripped_username,
        password=hashed_password,
        role="user"
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="The username already exists!"
        )

    return new_user

