"""Main application file for Vocabulary Builder."""

import gettext
import os
from enum import Enum
from pathlib import Path

import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from src.db.crud import create_user, get_random_word, get_user_by_username
from src.db.database import SessionLocal
from src.models import UserCreate


app = FastAPI()


class LanguageModel(str, Enum):
    ru = "ru"
    fr = "fr"


def get_db():
    """
    Provides a database session for dependency injection.

    :yields: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="src/templates")


def _(language: str):
    """
    Retrieves the gettext translation function for the specified language.

    :param language: Language code (e.g., 'ru', 'fr').
    :return: The translation function for the specified language.
    """
    try:
        translations = gettext.translation(
            domain="translations",
            localedir=os.path.join(os.path.dirname(__file__), "locales"),
            languages=[language],
        )
    except FileNotFoundError:
        translations = gettext.NullTranslations()
    return translations.gettext


def fetch_random_word_data(db: Session):
    """
    Fetches a random word and its translations from the database.

    :param db: Database session.
    :return: A dictionary with word data.
    """
    random_row = get_random_word(db)
    data = {
        "word": random_row.word,
        "translated_word": random_row.translated_word,
        "context": random_row.context,
        "translated_context": random_row.translated_context,
    }
    return data


@app.get("/", response_class=RedirectResponse)
def redirect_to_ru():
    """
    Redirects the root URL ('/') to the Russian language version ('/ru').

    :return: Redirect response to '/ru'.
    """
    return RedirectResponse(url="/ru")


@app.get("/{language}", response_class=HTMLResponse)
def get_main_page_in_language(
    request: Request, language: LanguageModel, db: Session = Depends(get_db)
):
    """
    Serves the main page in the specified language.

    :param request: HTTP request.
    :param language: Language code (e.g., 'ru', 'fr').
    :param db: Database session dependency.
    :return: HTML response with the main page content in the specified language.
    """
    context = fetch_random_word_data(db)
    context.update({"_": _(language)})
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@app.get("/{language}/new_word", response_class=JSONResponse)
def get_new_word(language: LanguageModel, db: Session = Depends(get_db)):
    """
    Fetches a new random word and returns it as a JSON response
    according to the specified language.

    :param language: Language code.
    :param db: Database session dependency.
    :return: JSON response with the new word data.
    """
    data = fetch_random_word_data(db)
    return data


def get_hashed_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    :param user: User registration data.
    :param db: Database session dependency.
    :return: JSON response with a message.
    """
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(db, user.username, get_hashed_password(user.password))
    return {"message": "User registered successfully"}
