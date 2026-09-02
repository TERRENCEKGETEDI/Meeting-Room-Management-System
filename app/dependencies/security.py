from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/routes/users/login")


# Hash password, return hashed password
def hash_password(password: str):
    """
    Hash a plain-text password

    Args:
        password: the plaintext password to hash

    Returns:
        hashed password
    """
    return password_hash.hash(password)


# verity password, return boolean
def verify_password(password: str, hashed_password: str):
    """Verify if the plaintext message matches the hashed passsword

    Args:
        password (str): plaintext password
        hashed_password (str): the hashed password

    Returns:
        If the password matches return true else false
    """
    return password_hash.verify(password, hashed_password)


# get current user, return user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Get the currently authenticated user.
    """

    payload = decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    stmt = select(User).where(User.username == username)

    user = db.scalars(stmt).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# require admin
def require_admin(current_user: User = Depends(get_current_user)):
    """
    Verify that the current user has admin privileges.

    Args:
        current_user: The currently authenticated user.

    Returns:
        The current user if they have admin privileges.

    Raises:
        HTTPException: If the current user is not an admin.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )
    return current_user
