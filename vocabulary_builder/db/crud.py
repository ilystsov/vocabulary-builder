"""CRUD operations for interacting with the database."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from vocabulary_builder.db.models import (
    SemanticModel,
    TranslationModel,
    UserModel,
    WordModel,
)


def get_random_word(db: Session, language: str):
    """
    Fetches a random word from the database with translation information for the
    specified language.

    :param db: The database session.
    :param language: The target language for the translation.
    :return: A tuple containing the random word and its associated semantics and
        translations.
    """
    # Select a random word
    stmt = select(WordModel).order_by(func.random()).limit(1)
    random_word = db.scalars(stmt).first()

    if not random_word:
        return None, None

    # Fetch translations for the specified language
    stmt = (
        select(SemanticModel, TranslationModel)
        .join(TranslationModel, SemanticModel.id == TranslationModel.semantic_id)
        .where(
            SemanticModel.word_id == random_word.id,
            TranslationModel.language == language,
        )
    )
    results = db.execute(stmt).all()

    return random_word, results


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
