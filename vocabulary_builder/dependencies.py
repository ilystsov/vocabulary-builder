from vocabulary_builder.db.database import SessionLocal


def get_db():
    """
    Provide a database session for dependency injection.

    :yields: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
