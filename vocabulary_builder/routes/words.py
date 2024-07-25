from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from vocabulary_builder.dependencies import get_db
from vocabulary_builder.utils.word_info import fetch_random_word_data


router = APIRouter()


@router.get("/new_word", response_class=JSONResponse)
def get_new_word(db: Session = Depends(get_db)):
    """
    Fetch a new random word and return it as a JSON response.

    :param language: Language code.
    :param db: Database session dependency.
    :return: JSON response with the new word data.
    """
    word_data = fetch_random_word_data(db)
    if word_data:
        return word_data
    return {"message": "No word found"}
