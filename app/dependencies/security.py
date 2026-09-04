from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


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
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):
    """
    Get the currently authenticated user.
    """

    payload = decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    stmt = select(User).where(User.username == username)

    user = session.scalars(stmt).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# require admin

# The routes currently use require_admin() only to check permissions; they do not use
# its return value. Please remove its return statement and declare this dependency in
# the route decorators, as shown below. This makes the purpose of the dependency clear
# and removes unused current_user parameters from the route functions. See:
#
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
#
# The dependencies argument tells FastAPI to run these checks before calling the route
# function. Their return values are not passed to the function:
#
#    @router.post(
#        "/",
#        dependencies=[Depends(require_admin)],
#        response_model=RoomResponse,
#        status_code=201
#    )
#    def add_room(
#        room: RoomCreate,
#        session: Session = Depends(get_db),  # noqa: B008
#    ):
#        ...
#
# Optionally, define the Depends object once and reuse it in the route decorators:
#
#    RequireAdminDep = Depends(require_admin)
#
# Then use it in the route:
#
#    @router.post(
#        "/",
#        dependencies=[RequireAdminDep],
#        response_model=RoomResponse,
#        status_code=201
#    )
#    def add_room(
#        room: RoomCreate,
#        session: Session = Depends(get_db),  # noqa: B008
#    ):
#        ...
#
# Apply the same approach to routes that use get_current_user() only to require
# authentication. Keep that function's return statement: routes that need the user
# object should still receive it through a function parameter with Depends.

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
