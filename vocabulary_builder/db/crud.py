"""CRUD operations for interacting with the database."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from vocabulary_builder.db.models import UserModel, WordModel


def get_random_word(db: Session):
    """
    Fetches a random word from the database.

    :param db: The database session.
    :return: The random word record from the database.
    """
    # Select a random word
    stmt = select(WordModel).order_by(func.random()).limit(1)
    random_word = db.scalars(stmt).first()

    return random_word


def create_user(db: Session, username: str, hashed_password: str) -> UserModel:
    """
    Creates a new user in the database.

    :param db: The database session.
    :param username: The username of the new user.
    :param password: The plain text password of the new user.
    :return: The created user record.
    """
    user = UserModel(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return user


def get_user_by_username(db: Session, username: str) -> UserModel:
    stmt = select(UserModel).where(UserModel.username == username)
    return db.scalars(stmt).first()
