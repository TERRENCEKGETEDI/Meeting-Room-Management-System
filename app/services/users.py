from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.roles import UserRole
from app.auth.security import create_access_token, hash_password, verify_password
from app.models.users import User
from app.schemas.user import UserCreate


async def create_user_services(
    user: UserCreate,
    session: AsyncSession
):
    """
    Create a new user.

    Args:
        user: UserCreate object containing username and password
        session: AsyncSession for database interaction

    Returns:
        new_user: The created user
    """
    try:
        new_user = User(
            username=user.username,
            password=hash_password(user.password),
            role=UserRole.USER.value
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )


async def login_services(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession
):
    """
    Login function for user authentication

    Args:
        form_data: OAuth2PasswordRequestForm containing username and password
        session: AsyncSession for database interaction

    Returns:
        access_token: JWT access token for authenticated user
    """
    stmt = select(User).where(
        User.username == form_data.username
    )
    result = await session.execute(stmt)
    existing_user = result.scalar()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        existing_user.username
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
