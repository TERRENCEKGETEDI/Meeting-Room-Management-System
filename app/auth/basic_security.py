
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.users import User

security = HTTPBasic()


async def basic_auth(
        credentials: HTTPBasicCredentials = Depends(security),  # noqa: B008
        session: AsyncSession = Depends(get_db)  # noqa: B008
):
    credential_exp = HTTPException(
        status_code=401, detail="Invalid username or password"
    )
    
    stmt = select(User).where(
        User.username == credentials.username
    )
    results = await session.execute(stmt)
    user = results.scalar()
    if user is None:
        raise credential_exp

    if credentials.username != user.username:
        raise credential_exp

    if credentials.password != user.password:
        raise credential_exp

    return user.role
