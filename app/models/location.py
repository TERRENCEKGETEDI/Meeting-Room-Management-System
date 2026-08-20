"""
SQLAlchemy ORM MODEL fro the location entity 

  The module is a table model for the Location class ,that will be used to map the tabe in the database to our python code
"""
from sqlalchemy import Mapped, mapped_column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    location_id: Mapped[int] = mapped_column(primary_key=True) # primary key of the table / other tables use a foregin key referencing this primary key
    location_name: Mapped[str] = mapped_column(nullable=False)
