import json
import sys
import uuid

from sqlalchemy.orm import Session

from vocabulary_builder.db.database import SessionLocal
from vocabulary_builder.db.models import ExampleModel, MeaningModel, WordModel


def create_audio_placeholder():
    return b"Audio Placeholder"


def load_words_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def populate_database(session: Session, words_data):
    for word_data in words_data:
        word = WordModel(
            id=uuid.uuid4(),
            word=word_data["word"],
            part_of_speech=word_data["part_of_speech"],
            transcription=word_data["transcription"],
            audio=create_audio_placeholder(),
        )
        session.add(word)
        session.commit()

        for meaning_data in word_data["meanings"]:
            meaning = MeaningModel(
                id=uuid.uuid4(),
                word_id=word.id,
                meaning=meaning_data["meaning"],
                meaning_language=meaning_data["language"],
            )
            session.add(meaning)
            session.commit()

            for example_data in meaning_data["examples"]:
                example = ExampleModel(
                    id=uuid.uuid4(),
                    meaning_id=meaning.id,
                    example=example_data["example"],
                    example_translation=example_data["translation"],
                    example_translation_language=example_data["language"],
                )
                session.add(example)

        session.commit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: dp_populate.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    words_data = load_words_from_json(json_path)

    session = SessionLocal()
    populate_database(session, words_data)
    session.close()
