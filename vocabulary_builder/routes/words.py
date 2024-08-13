"""Module providing an API route to fetch a new random word"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vocabulary_builder.dependencies import get_db
from vocabulary_builder.utils.word_info import fetch_random_word_data


router = APIRouter()


@router.get("/new_word")
def get_new_word(db: Session = Depends(get_db)) -> dict:
    """
    Fetch a new random word and return it as a JSON response.

    :param db: Database session dependency.
    :return: JSON response with the new word data, or a message if no word is found.
    """
    word_data = fetch_random_word_data(db)
    if word_data:
        return word_data
    return {"message": "No word found"}
