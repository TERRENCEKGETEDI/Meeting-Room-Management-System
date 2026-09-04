from app.database.database import SessionLocal

# Please use the session as a context manager to simplify its cleanup:
#
# def get_db():
#     with SessionLocal() as session:
#         yield session
#
# This provides the same cleanup as the current try/finally block, with less code.
#
# When FastAPI cleans up the dependency, execution leaves the with block and the
# session is automatically closed, including when an exception has occurred.
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
