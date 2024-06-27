"""Main application file for Vocabulary Builder."""

import gettext
import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jwt import InvalidTokenError
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from vocabulary_builder.db.crud import (
    create_user,
    get_all_saved_words_for_user,
    get_random_word,
    get_user_by_username,
    remove_word_for_user,
    save_word_for_user,
)
from vocabulary_builder.db.database import SessionLocal
from vocabulary_builder.db.models import WordModel
from vocabulary_builder.exceptions import (
    CredentialsException,
    IncorrectUsernamePasswordException,
    UserNotFound,
    WordNotFound,
)
from vocabulary_builder.models import UserBase, WordBase


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """Custom OAuth2 password bearer class that supports cookies."""

    async def __call__(self, request: Request) -> str:
        """
        Retrieve the access token from the request cookies.

        :param request: HTTP request.
        :return: Access token.
        :raises HTTPException: If the access token is not found in cookies.
        """
        authorization: str = request.cookies.get("access_token")
        if not authorization:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return authorization


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")


app = FastAPI()


class LanguageModel(str, Enum):
    """Enumeration of supported languages."""

    ru = "ru"
    uk = "uk"
    fr = "fr"
    de = "de"


def get_db():
    """
    Provide a database session for dependency injection.

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
    Retrieve the gettext translation function for the specified language.

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


def format_word_info(word: WordModel):
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


@app.get("/", response_class=HTMLResponse)
def get_main_page_in_language(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    db: Session = Depends(get_db),
):
    """
    Serve the main page in the specified language.

    :param request: HTTP request.
    :param language: Language code (e.g., 'ru', 'fr').
    :param db: Database session dependency.
    :return: HTML response with the main page content in the specified language.
    """
    context = fetch_random_word_data(db)
    context.update({"_": _(language)})
    context.update({"language": language.value})
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@app.get("/new_word", response_class=JSONResponse)
def get_new_word(language: LanguageModel, db: Session = Depends(get_db)):
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


def get_hashed_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    :param password: Plain text password.
    :return: Hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    :param plain_password: Plain text password.
    :param hashed_password: Hashed password.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> UserBase | bool:
    """
    Authenticate a user by username and password.

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
    return UserBase(username=username, user_id=str(user.id))


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT access token.

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
    Get the current user based on the JWT token.

    :param token: JWT token.
    :param db: Database session dependency.
    :return: Current user.
    """
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if username is None or user_id is None:
            raise CredentialsException
    except InvalidTokenError:
        raise CredentialsException
    user = get_user_by_username(db, username)
    if user is None:
        raise CredentialsException
    return UserBase(username=username, user_id=user_id)


@app.get("/signup", response_class=HTMLResponse)
def register_page(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    db: Session = Depends(get_db),
):
    """
    Serve the registration page.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the registration page.
    """
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={"_": _(language), "language": language.value},
    )


@app.post("/signup")
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
    return RedirectResponse(url=f"/login?language={language}", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, language: str = "ru"):
    """
    Serve the login page.

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
) -> RedirectResponse:
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
        data={"username": user.username, "user_id": user.user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response = RedirectResponse(url=f"/learn?language={language}", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
    )
    return response


@app.get("/learn")
async def learn(
    language: LanguageModel,
    current_user: UserBase = Depends(get_current_user),
):
    """
    Endpoint to learn a new word for the current user.

    :param language: Language code.
    :param current_user: Current user dependency.
    :return: JSON response with the new word data.
    """
    return {
        f"{current_user.username}'s new word (user's id) "
        f"{current_user.user_id}": "issue"
    }


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Redirect to the error page if the status code is 404 or 422.

    :param request: HTTP request.
    :param exc: Starlette HTTP exception.
    :return: JSON response or redirect to error page.
    """
    if exc.status_code in {404, 422}:
        return RedirectResponse(url="/error")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/error", response_class=HTMLResponse)
def error_page(request: Request):
    """
    Serve the error page.

    :param request: HTTP request.
    :return: HTML response with the error page.
    """
    return """
    <html>
        <head>
            <script>
                var userLanguage = localStorage.getItem('language') || 'ru';
                window.location.href = '/page_not_found?language=' + userLanguage;
            </script>
        </head>
        <body>
        </body>
    </html>
    """


@app.get("/page_not_found")
async def page_not_found(request: Request, language: str = "ru"):
    """
    Serve the error page with a custom image based on the status code and language.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the error page.
    """
    return templates.TemplateResponse(
        request=request,
        name="page_not_found.html",
        context={"_": _(language), "language": language},
    )


@app.post("/users/{user_id}/words")
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


@app.delete("/users/{user_id}/words")
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


@app.get("/users/{user_id}/words")
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


@app.get("/favorites")
async def get_favorite_words(
    request: Request,
    language: LanguageModel,
    current_user: UserBase = Depends(get_current_user),
):
    """
    Retrieve favorite words for the current user.

    :param request: HTTP request.
    :param language: Language code.
    :param current_user: Current user dependency.
    :return: HTML response with the favorite words.
    """
    return templates.TemplateResponse(
        request=request,
        name="favorites.html",
        context={
            "_": _(language),
            "language": language,
            "username": current_user.username,
            "user_id": current_user.user_id,
        },
    )


def replace_query_param(url, param: str, value: str) -> str:
    if not isinstance(url, str):
        url = str(url)

    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)
    query_params[param] = value
    new_query_string = urlencode(query_params, doseq=True)
    new_url = url_parts._replace(query=new_query_string).geturl()
    return new_url


def startup_event():
    templates.env.filters["replace_query_param"] = replace_query_param


app.add_event_handler("startup", startup_event)
