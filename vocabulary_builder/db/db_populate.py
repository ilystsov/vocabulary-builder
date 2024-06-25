import json
import sys
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from vocabulary_builder.db.database import SessionLocal
from vocabulary_builder.db.models import (
    ExampleModel,
    ExampleTranslationModel,
    SemanticModel,
    TranslationModel,
    WordModel,
)


def create_audio_placeholder():
    return b"Audio Placeholder"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def populate_database(data, session: Session):
    total_words = len(data)
    successful_words = 0

    for word_data in data:
        try:
            word = WordModel(
                id=uuid.uuid4(),
                word=word_data["word"],
                part_of_speech=word_data["part_of_speech"],
                transcription=word_data["transcription"],
                # Assuming the audio is base64 encoded binary data
                # audio=word_data['audio'].encode()
                audio=create_audio_placeholder(),
            )
            session.add(word)
            session.flush()  # Flush to get the word.id

            for semantic_data in word_data["semantics"]:
                semantic = SemanticModel(id=uuid.uuid4(), word_id=word.id)
                session.add(semantic)
                session.flush()  # Flush to get the semantic.id

                for example_text in semantic_data["examples"]:
                    example = ExampleModel(
                        id=uuid.uuid4(), semantic_id=semantic.id, example=example_text
                    )
                    session.add(example)

                for lang, translation_data in semantic_data["translations"].items():
                    translation = TranslationModel(
                        id=uuid.uuid4(),
                        semantic_id=semantic.id,
                        language=lang,
                        word=translation_data["word"],
                    )
                    session.add(translation)
                    session.flush()  # Flush to get the translation.id

                    for translated_example_text in translation_data["examples"]:
                        example_translation = ExampleTranslationModel(
                            id=uuid.uuid4(),
                            translation_id=translation.id,
                            example=translated_example_text,
                        )
                        session.add(example_translation)

            session.commit()  # Commit after adding all data related to one word
            successful_words += 1
        except Exception as e:
            print(f"Error populating database for word '{word_data['word']}': {e}")
            session.rollback()
            continue

    print(
        f"Successfully added {successful_words} out of {total_words} words "
        "to the database."
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: db_populate.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    if not Path(json_file_path).is_file():
        print(f"File not found: {json_file_path}")
        sys.exit(1)

    data = load_json(json_file_path)

    session = SessionLocal()
    try:
        populate_database(data, session)
    finally:
        session.close()


if __name__ == "__main__":
    main()
