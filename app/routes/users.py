from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.dependencies.database import get_db
from app.dependencies.security import verify_password
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


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

    return create_access_token(
        existing_user.username
    )
    