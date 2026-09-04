"""Security module"""
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.roles import UserRole
from app.database.dependencies import get_db
from app.models.users import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hashes the password and return the hashed password

    Args:
        password: The plain text password

    Returns:
        password_hash: the hashed password
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies the entered password against the stored password

    Args:
        password: plain entered password
        hashed_password: the hashed password

    Return:
        status: True if match or False if not
    """
    return password_hash.verify(password, hashed_password)


def create_access_token(username: str) -> str:
    """
    Creates token for the user to login

    Args:
        username: username of the user

    Returns:
        token: the generated token
    """
    expire = datetime.now(timezone.utc) + timedelta(  # noqa: UP017
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)  # noqa: B008
) -> User:
    """
    Get current user details

    Args:
        token: token of assigned to the user
        session: database session

    Returns:
        user: details of the user
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    stmt = select(User).where(
        User.username == username
    )
    results = await session.execute(stmt)
    user = results.scalar()
    if user is None:
        raise credentials_exception

    return user


def require_admin(
        current_user: User = Depends(get_current_user)  # noqa: B008
) -> User:
    """
    Verifies that the user has admin privileges

    Args:
        user: receives user object

    Returns:
        user: returns the user details
    """
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user
