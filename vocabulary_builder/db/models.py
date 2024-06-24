"""
Database models.
"""

import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vocabulary_builder.db.database import BaseModel


class WordModel(BaseModel):
    """
    Represents a word with its basic attributes.

    :param id: Primary key.
    :param word: The word in the target language.
    :param part_of_speech: The part of speech of the word.
    :param transcription: The phonetic transcription of the word.
    :param audio: The audio pronunciation of the word in binary format.
    :param meanings: The list of meanings associated with the word.
    """

    __tablename__ = "words"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word: Mapped[str] = mapped_column(nullable=False)
    part_of_speech: Mapped[str] = mapped_column(nullable=False)
    transcription: Mapped[str] = mapped_column(nullable=False)
    audio: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    meanings: Mapped[list["MeaningModel"]] = relationship()


class MeaningModel(BaseModel):
    """
    Represents a meaning of a word.

    :param id: Primary key.
    :param word_id: Foreign key referencing the associated word.
    :param meaning: The meaning of the word in a specific language.
    :param meaning_language: The language of the meaning.
    :param examples: The list of examples demonstrating the use of the meaning.
    """

    __tablename__ = "meanings"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word_id: Mapped[UUID] = mapped_column(ForeignKey("words.id"), nullable=False)
    meaning: Mapped[str] = mapped_column(nullable=False)
    meaning_language: Mapped[str] = mapped_column(nullable=False)
    examples: Mapped[list["ExampleModel"]] = relationship()


class ExampleModel(BaseModel):
    """
    Represents an example sentence demonstrating the use of a word.

    :param id: Primary key.
    :param meaning_id: Foreign key referencing the associated meaning.
    :param example: The example sentence in the target language.
    :param example_translation: The translation of the example sentence.
    :param example_translation_language: The language of the example translation.
    """

    __tablename__ = "examples"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    meaning_id: Mapped[UUID] = mapped_column(ForeignKey("meanings.id"), nullable=False)
    example: Mapped[str] = mapped_column(nullable=False)
    example_translation: Mapped[str] = mapped_column(nullable=False)
    example_translation_language: Mapped[str] = mapped_column(nullable=False)


class UserModel(BaseModel):
    """
    Represents a user in the system.

    :param id: Primary key.
    :param username: The username of the user.
    :param hashed_password: The hashed password of the user.
    """

    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
