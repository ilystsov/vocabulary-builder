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


def delete_word(word: str, session: Session):
    try:
        # Найти все записи WordModel для указанного слова
        words = session.query(WordModel).filter_by(word=word).all()

        for word_record in words:
            # Найти все связанные записи SemanticModel
            semantics = (
                session.query(SemanticModel).filter_by(word_id=word_record.id).all()
            )

            for semantic in semantics:
                # Найти и удалить все связанные записи ExampleModel
                examples = (
                    session.query(ExampleModel).filter_by(semantic_id=semantic.id).all()
                )
                for example in examples:
                    session.delete(example)

                # Найти и удалить все связанные записи TranslationModel
                translations = (
                    session.query(TranslationModel)
                    .filter_by(semantic_id=semantic.id)
                    .all()
                )
                for translation in translations:
                    # Найти и удалить все связанные записи ExampleTranslationModel
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
    try:
        # Удалить все записи из таблиц, начиная с наиболее вложенных
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
