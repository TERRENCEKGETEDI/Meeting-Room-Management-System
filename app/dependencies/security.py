from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.roles import UserRole
from app.models.user import User

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Password validation
def password_validation(password: str):
    lower_cases = 0
    upper_cases = 0
    num_digits = 0
    special_chars = 0
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weak password, length must be 8 characters or more"
        )

    for char in password:
        if char.isdigit():
            num_digits += 1
        if char.islower():
            lower_cases += 1
        if char.isupper():
            upper_cases += 1
        if not char.isalnum():
            special_chars += 1

    if (
        lower_cases < 1
        or upper_cases < 1
        or num_digits < 1
        or special_chars < 1
    ):
        message = (
            "Invalid password, at least 1 small letters, 1 capital letter, "
            "1 digit, 1 special character"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


# Hash password, return hashed password
def hash_password(password: str):
    """
    Hash a plain-text password

    Args:
        password: the plaintext password to hash

    Returns:
        hashed password
    """
    password_validation(password)
    return password_hash.hash(password)


# verity password, return boolean
def verify_password(password: str, hashed_password: str):
    """Verify if the plaintext message matches the hashed password

    Args:
        password (str): plaintext password
        hashed_password (str): the hashed password

    Returns:
        If the password matches return true else false
    """
    return password_hash.verify(password, hashed_password)


# get current user, return user


def get_current_user(
    session: Annotated[Session, Depends(get_db)],
    token: str = Depends(oauth2_scheme)
):
    """
        Get the currently authenticated user.

        Args:
            session: database session
            token: user token
    """

    payload = decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    stmt = select(User).where(User.username == username)

    user = session.scalars(stmt).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# require admin
def require_admin(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Verify that the current user has admin privileges.

    Args:
        current_user: The currently authenticated user.

    Raises:
        HTTPException: If the current user is not an admin.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
