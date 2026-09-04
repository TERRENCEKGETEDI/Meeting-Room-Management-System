from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class User(Base):
    """
    Represent Users stored in the database

    Attributes:
        id: Primary Key
        full_name: the full name of the user
        username: the username of the user
        password: the password of the user
        role: the role of the user (admin or user)
    """
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    full_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    # Please restrict role to the supported values, currently 'user' and 'admin', so
    # invalid roles cannot be stored. A separate roles table with a foreign key may be
    # useful in future, but restricting this column is sufficient for this project.
    #
    # Investigate using a Python StrEnum to define the supported roles. Use the same
    # enum in the SQLAlchemy mapping, schemas.user.UserResponse.role, and any request
    # parameters or Pydantic fields that accept roles. Use enum members throughout the
    # code instead of string literals. For example, once the ORM returns enum members:
    #
    #     if user.role is UserRole.ADMIN:
    #
    # Sharing one definition keeps the supported roles consistent across these layers
    # and avoids typos in string comparisons. Adding a role then starts with updating
    # the enum, rather than maintaining separate lists of allowed values.
    #
    # Configure the database enum or check constraint as well: a Python enum alone does
    # not constrain the existing String column. Changes to database constraints may
    # require a migration. The identity comparison above is appropriate only when the
    # ORM attribute contains an enum member; it will not work with a plain string.
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="user"
    )
