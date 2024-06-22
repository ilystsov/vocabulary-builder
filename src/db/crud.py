"""CRUD operations for interacting with the database."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import WordModel


def get_random_word(db: Session):
    """
    Fetches a random word from the database.

    :param db: The database session.
    :return: A random word record from the database.
    """
    stmt = select(WordModel).order_by(func.random()).limit(1)
    random_row = db.scalars(stmt).first()
    return random_row
