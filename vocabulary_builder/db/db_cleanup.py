"""Database cleanup utility for deleting words and related records."""
import sys

from sqlalchemy.orm import Session

from vocabulary_builder.db.database import SessionLocal
from vocabulary_builder.db.models import (
    ExampleModel,
    ExampleTranslationModel,
    SemanticModel,
    TranslationModel,
    WordModel,
)


def delete_word(word: str, session: Session) -> None:
    """
    Delete all records related to a specific word from the database.

    :param word: Word to delete.
    :param session: SQLAlchemy session object.
    """
    try:
        words = session.query(WordModel).filter_by(word=word).all()

        for word_record in words:
            semantics = (
                session.query(SemanticModel).filter_by(word_id=word_record.id).all()
            )

            for semantic in semantics:
                examples = (
                    session.query(ExampleModel).filter_by(semantic_id=semantic.id).all()
                )
                for example in examples:
                    session.delete(example)

                translations = (
                    session.query(TranslationModel)
                    .filter_by(semantic_id=semantic.id)
                    .all()
                )
                for translation in translations:
                    example_translations = (
                        session.query(ExampleTranslationModel)
                        .filter_by(translation_id=translation.id)
                        .all()
                    )
                    for example_translation in example_translations:
                        session.delete(example_translation)
                    session.delete(translation)

                session.delete(semantic)

            session.delete(word_record)

        session.commit()
        print(
            f"Successfully deleted all records for the word '{word}' from the database."
        )
    except Exception as e:
        session.rollback()
        print(f"Error deleting records for the word '{word}': {e}")


def delete_all_words(session: Session):
    """
    Delete all words and related records from the database.

    :param session: SQLAlchemy session object.
    """
    try:
        session.query(ExampleTranslationModel).delete()
        session.query(ExampleModel).delete()
        session.query(TranslationModel).delete()
        session.query(SemanticModel).delete()
        session.query(WordModel).delete()
        session.commit()
        print("Successfully deleted all words and related records from the database.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting all words: {e}")


def main():
    """Delete words from the database."""
    if len(sys.argv) != 2:
        print("Usage: db_cleanup.py <word|--all>")
        sys.exit(1)

    argument = sys.argv[1]

    session = SessionLocal()
    try:
        if argument == "--all":
            delete_all_words(session)
        else:
            delete_word(argument, session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
