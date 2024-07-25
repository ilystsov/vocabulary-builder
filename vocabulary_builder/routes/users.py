from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from requests import Session

from vocabulary_builder.db.crud import (
    get_all_saved_words_for_user,
    remove_word_for_user,
    save_word_for_user,
)
from vocabulary_builder.dependencies import get_db
from vocabulary_builder.exceptions import UserNotFound, WordNotFound
from vocabulary_builder.models import WordBase
from vocabulary_builder.utils.word_info import format_word_info


router = APIRouter()


@router.post("/users/{user_id}/words")
async def save_word(user_id: UUID4, word: WordBase, db: Session = Depends(get_db)):
    """
    Save a word for the user.

    :param user_id: User ID.
    :param word: Word data.
    :param db: Database session dependency.
    :return: JSON response with a success message.
    """
    try:
        save_word_for_user(db, word.word_id, user_id)
    except (UserNotFound, WordNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Word saved successfully."}


@router.delete("/users/{user_id}/words")
async def remove_word(user_id: UUID4, word: WordBase, db: Session = Depends(get_db)):
    """
    Remove a word for the user.

    :param user_id: User ID.
    :param word: Word data.
    :param db: Database session dependency.
    :return: JSON response with a success message.
    """
    try:
        remove_word_for_user(db, word.word_id, user_id)
    except (UserNotFound, WordNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Word removed successfully."}


@router.get("/users/{user_id}/words")
async def get_saved_words(user_id: UUID4, db: Session = Depends(get_db)) -> list[dict]:
    """
    Retrieve saved words for the user.

    :param user_id: User ID.
    :param db: Database session dependency.
    :return: List of dictionaries containing saved words information.
    """
    try:
        saved_words = get_all_saved_words_for_user(db, user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    formatted_words = []
    for word in saved_words:
        formatted_words.append(format_word_info(word))
    return formatted_words
