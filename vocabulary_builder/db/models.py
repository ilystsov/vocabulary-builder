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
    Represents an English word with its part of speech, transcription, and
    pronunciation audio.

    :param id: Primary key.
    :param word: The English word.
    :param part_of_speech: The part of speech of the word.
    :param transcription: The transcription of the word.
    :param audio: The pronunciation audio of the word (binary data).
    :param semantics: List of semantic meanings of the word.
    """

    __tablename__ = "words"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word: Mapped[str] = mapped_column(nullable=False)
    part_of_speech: Mapped[str] = mapped_column(nullable=False)
    transcription: Mapped[str] = mapped_column(nullable=False)
    audio: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    semantics: Mapped[list["SemanticModel"]] = relationship()


class SemanticModel(BaseModel):
    """
    Represents a semantic meaning of an English word.

    :param id: Primary key.
    :param word_id: Foreign key to the associated word.
    :param translations: List of translations for this semantic meaning.
    :param examples: List of usage examples for this semantic meaning.
    """

    __tablename__ = "semantics"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word_id: Mapped[UUID] = mapped_column(ForeignKey("words.id"), nullable=False)
    translations: Mapped[list["TranslationModel"]] = relationship()
    examples: Mapped[list["ExampleModel"]] = relationship()


class ExampleModel(BaseModel):
    """
    Represents a usage example of an English word in a specific semantic context.

    :param id: Primary key.
    :param semantic_id: Foreign key to the associated semantic meaning.
    :param example: The example text.
    """

    __tablename__ = "examples"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    semantic_id: Mapped[UUID] = mapped_column(
        ForeignKey("semantics.id"), nullable=False
    )
    example: Mapped[str] = mapped_column(nullable=False)


class TranslationModel(BaseModel):
    """
    Represents a translation of an English word's semantic meaning into another
    language.

    :param id: Primary key.
    :param semantic_id: Foreign key to the associated semantic meaning.
    :param language: The target language of the translation.
    :param word: The translated word.
    :param examples: List of translations for the usage examples in this semantic
        context.
    """

    __tablename__ = "translations"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    semantic_id: Mapped[UUID] = mapped_column(
        ForeignKey("semantics.id"), nullable=False
    )
    language: Mapped[str] = mapped_column(nullable=False)
    word: Mapped[str] = mapped_column(nullable=False)
    examples: Mapped[list["ExampleTranslationModel"]] = relationship()


class ExampleTranslationModel(BaseModel):
    """
    Represents a translation of a usage example of an English word into another
    language.

    :param id: Primary key.
    :param translation_id: Foreign key to the associated translation.
    :param example: The translated example text.
    """

    __tablename__ = "examples_translations"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    translation_id: Mapped[UUID] = mapped_column(
        ForeignKey("translations.id"), nullable=False
    )
    example: Mapped[str] = mapped_column(nullable=False)


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
