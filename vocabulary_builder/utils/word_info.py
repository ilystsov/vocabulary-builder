"""
This module provides functions to format word data and
fetch random words from the database.
"""
from sqlalchemy.orm import Session

from vocabulary_builder.db.crud import get_random_word
from vocabulary_builder.db.models import WordModel


def format_word_info(word: WordModel) -> dict:
    """
    Format word information into a dictionary.

    :param word: Word model instance.
    :return: Dictionary containing formatted word information.
    """
    word_info = {
        "word_id": word.id,
        "word": word.word,
        "part_of_speech": word.part_of_speech,
        "transcription": word.transcription,
        "audio": word.audio,
        "semantics": [],
    }

    for semantic in word.semantics:
        semantic_info = {
            "translations": {},
            "examples": [example.example for example in semantic.examples],
        }
        for translation in semantic.translations:
            translation_info = {
                "word": translation.word,
                "examples": [
                    ex_translation.example for ex_translation in translation.examples
                ],
            }
            semantic_info["translations"][translation.language] = translation_info

        word_info["semantics"].append(semantic_info)
    return word_info


def fetch_random_word_data(db: Session) -> dict:
    """
    Fetch a random word and formats it as a JSON response.

    :param db: The database session.
    :return: A dictionary containing the word and its translation information.
    """
    random_word = get_random_word(db)

    if not random_word:
        return {}

    word_info = format_word_info(random_word)
    return word_info
