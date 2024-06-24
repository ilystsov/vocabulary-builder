"""Main application file for Vocabulary Builder."""

import gettext
import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from vocabulary_builder.db.crud import (
    create_user,
    get_random_word,
    get_user_by_username,
)
from vocabulary_builder.db.database import SessionLocal
from vocabulary_builder.exceptions import (
    CredentialsException,
    IncorrectUsernamePasswordException,
)
from vocabulary_builder.models import Token, UserBase


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

templates = Jinja2Templates(directory="vocabulary_builder/templates")


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
    random_word = get_random_word(db)
    if not random_word:
        return None

    meanings = []
    for meaning in random_word.meanings:
        examples = [
            {
                "example": example.example,
                "example_translation": example.example_translation,
                "example_translation_language": example.example_translation_language,
            }
            for example in meaning.examples
        ]
        meanings.append(
            {
                "meaning": meaning.meaning,
                "meaning_language": meaning.meaning_language,
                "examples": examples,
            }
        )

    data = {
        "word": random_word.word,
        "part_of_speech": random_word.part_of_speech,
        "transcription": random_word.transcription,
        "audio": random_word.audio,
        "meanings": meanings,
    }
    return data


@app.get("/", response_class=HTMLResponse)
def get_main_page_in_language(
    request: Request, language: LanguageModel = "ru", db: Session = Depends(get_db)
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


@app.get("/new_word", response_class=JSONResponse)
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
    """
    Hashes a plain text password using bcrypt.

    :param password: Plain text password.
    :return: Hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    :param plain_password: Plain text password.
    :param hashed_password: Hashed password.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> UserBase | bool:
    """
    Authenticates a user by username and password.

    :param username: Username.
    :param password: Password.
    :param db: Database session dependency.
    :return: User representation if authentication is successful, False otherwise.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return UserBase(username=username)


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Creates a JWT access token.

    :param data: Data to encode in the token.
    :param expires_delta: Token expiration time.
    :return: Encoded JWT token.
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserBase:
    """
    Gets the current user based on the JWT token.

    :param token: JWT token.
    :param db: Database session dependency.
    :return: Current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
    except InvalidTokenError:
        raise CredentialsException
    user = get_user_by_username(db, username)
    if user is None:
        raise CredentialsException
    return UserBase(username=username)


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, language: str = "ru"):
    """
    Serves the registration page.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the registration page.
    """
    return templates.TemplateResponse(
        "register.html", {"request": request, "language": language, "_": _(language)}
    )


@app.post("/register")
async def register_user(
    username: str = Form(...),
    password: str = Form(...),
    language: str = Form("ru"),
    db: Session = Depends(get_db),
):
    """
    Endpoint to register a new user.

    :param username: Username from form data.
    :param password: Password from form data.
    :param language: Language from form data (default is 'ru').
    :param db: Database session dependency.
    :return: JSON response with a message.
    """
    db_user = get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(db, username, get_hashed_password(password))
    return {"message": "User registered successfully"}


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, language: str = "ru"):
    """
    Serves the login page.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the login page.
    """
    return templates.TemplateResponse(
        "login.html", {"request": request, "language": language, "_": _(language)}
    )


@app.post("/login")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    language: str = Form("ru"),
    db: Session = Depends(get_db),
) -> Token:
    """
    Endpoint to log in and get an access token.

    :param username: Username from form data.
    :param password: Password from form data.
    :param language: Language from form data (default is 'ru').
    :param db: Database session dependency.
    :return: JWT access token.
    """
    user = authenticate_user(username, password, db)
    if not user:
        raise IncorrectUsernamePasswordException
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/learn")
async def learn(
    language: LanguageModel,
    current_user: UserBase = Depends(get_current_user),
):
    return {f"{current_user.username}'s new word": "issue"}
