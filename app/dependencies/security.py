
from fastapi import Depends , HTTPException

from app.models.user import User

# Hash password, return hashed password

# verity password, return boolean

# get current user, return user


# require admin



def require_admin(
     current_user :User = Depends(get_current_user)
):
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