from database.database import SessionLocal


def get_db():
    """
    Provide a database session and close it after the request.

    Yields:
        Session: Database session used by the request.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

