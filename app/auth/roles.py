"""Roles to user account"""
from enum import Enum


class UserRole(str, Enum):
    """Roles that are available

        Attributes:
            USER: user
            ADMIN: admin
    """
    USER = "user"
    ADMIN = "admin"
