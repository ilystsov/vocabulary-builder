"""
This module provides functions for dependency injection,
such as providing a database session.
"""
from sqlalchemy.orm import Session

from vocabulary_builder.db.database import SessionLocal


def get_db() -> Session:
    """
    Provide a database session for dependency injection.

    :yields: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
