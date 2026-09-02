# Hash password, return hashed password

# verity password, return boolean

# get current user, return user
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Get the currently authenticated user.
    """

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    stmt = select(User).where(User.id == int(user_id))

    user = db.scalars(stmt).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# require admin
