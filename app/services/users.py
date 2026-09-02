from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.dependencies.security import verify_password
from app.models.user import User


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
    