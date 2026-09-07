from app.database.database import SessionLocal


def get_db():
    """
    Provide a database session and close it after the request.

    Yields:
        Session: Database session used by the request.
    """
    with SessionLocal() as session:
        yield session

