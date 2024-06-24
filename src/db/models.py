"""
Database models.
"""

import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import BaseModel


class Word(BaseModel):
    """
    Represents a word with its basic attributes.

    :param id: Primary key.
    :param word: The word in the original language.
    :param part_of_speech: The part of speech of the word.
    :param transcription: The transcription of the word.
    :param audio: The audio file of the word pronunciation.
    """

    __tablename__ = "words"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word: Mapped[str] = mapped_column(nullable=False)
    part_of_speech: Mapped[str] = mapped_column(nullable=False)
    transcription: Mapped[str] = mapped_column(nullable=False)
    audio: Mapped[LargeBinary] = mapped_column(nullable=False)
    translations: Mapped[list["Translation"]] = relationship(back_populates="word")


class Translation(BaseModel):
    """
    Represents a translation of a word.

    :param id: Primary key.
    :param word_id: Foreign key to the word.
    :param language: The language of the translation.
    :param translation: The translated word.
    """

    __tablename__ = "translations"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word_id: Mapped[UUID] = mapped_column(ForeignKey("words.id"), nullable=False)
    language: Mapped[str] = mapped_column(nullable=False)
    translation: Mapped[str] = mapped_column(nullable=False)
    word: Mapped["Word"] = relationship("Word", back_populates="translations")
    examples: Mapped[list["Example"]] = relationship(back_populates="translation")


class Example(BaseModel):
    """
    Represents an example usage of a translated word.

    :param id: Primary key.
    :param translation_id: Foreign key to the translation.
    :param example_eng: Example sentence in English.
    :param example_trans: Translated example sentence.
    """

    __tablename__ = "examples"
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    translation_id: Mapped[UUID] = mapped_column(
        ForeignKey("translations.id"), nullable=False
    )
    example_eng: Mapped[str] = mapped_column(nullable=False)
    example_trans: Mapped[str] = mapped_column(nullable=False)
    translation: Mapped["Translation"] = relationship(back_populates="examples")


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
