import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#load environment variables
load_dotenv()


#So instead of hard-coding these values, the application retrieves them from the environment
DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


engine = create_engine(DATABASE_URL)

#create database sessions using the engine.
SessionLocal = sessionmaker(bind=engine)

#It allows SQLAlchemy to understand those Python classes as database models.
class Base(DeclarativeBase):
    pass
