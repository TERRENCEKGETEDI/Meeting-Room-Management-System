"""User routes"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users import create_user_services, login_services

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
        "/",
        response_model=UserResponse,
        status_code=201)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
    Create a new user.

    Args:
        user: UserCreate object containing username and password
        session: AsyncSession for database interaction
    Returns:
        new_user: The created user
    """
    return await create_user_services(user, session)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    session: AsyncSession = Depends(get_db)  # noqa: B008
):
    """
    Login function for user authentication

    Args:
        form_data: OAuth2PasswordRequestForm containing username and password
        session: AsyncSession for database interaction
    Returns:
        access_token: JWT access token for authenticated user
    """
    return await login_services(form_data, session)