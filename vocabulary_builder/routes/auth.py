from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from vocabulary_builder.db.crud import create_user, get_user_by_username
from vocabulary_builder.dependencies import get_db
from vocabulary_builder.exceptions import IncorrectUsernamePasswordException
from vocabulary_builder.utils.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_hashed_password,
)
from vocabulary_builder.utils.translations import LanguageModel


router = APIRouter()


@router.post("/signup")
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


@router.post("/login")
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


@router.get("/logout")
async def logout(language: LanguageModel = LanguageModel.ru):
    """
    Endpoint to log out and remove the access token cookie.

    :param request: HTTP request.
    :param response: HTTP response.
    :param language: Language parameter (default is 'ru').
    :return: Redirect to the home page or login page.
    """
    response = RedirectResponse(url=f"/?language={language.value}", status_code=303)
    response.delete_cookie(key="access_token")
    return response
