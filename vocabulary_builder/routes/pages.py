"""Routes for rendering HTML pages"""
from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from vocabulary_builder.dependencies import get_db
from vocabulary_builder.models import UserBase
from vocabulary_builder.utils.auth import get_current_user
from vocabulary_builder.utils.translations import LanguageModel, _
from vocabulary_builder.utils.word_info import fetch_random_word_data


router = APIRouter()

templates = Jinja2Templates(directory="vocabulary_builder/templates")


@router.get("/")
def get_main_page_in_language(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """
    Serve the main page in the specified language.

    :param request: HTTP request.
    :param language: Language code (e.g., 'ru', 'fr').
    :param db: Database session dependency.
    :return: HTML response with the main page content in the specified language.
    """
    context = fetch_random_word_data(db)
    context.update({"_": _(language.value)})
    context.update({"language": language.value})
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context,
    )


@router.get("/signup")
def register_page(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
) -> HTMLResponse:
    """
    Serve the registration page.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the registration page.
    """
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={"_": _(language.value), "language": language.value},
    )


@router.get("/login")
def login_page(
    request: Request, language: LanguageModel = LanguageModel.ru
) -> HTMLResponse:
    """
    Serve the login page.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the login page.
    """
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"_": _(language.value), "language": language.value},
    )


@router.get("/learn")
def get_learn_page_in_language(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    current_user: UserBase = Depends(get_current_user),
) -> HTMLResponse:
    """
    Endpoint to learn a new word for the current user.

    :param request: HTTP request.
    :param language: Language code.
    :param current_user: Current user dependency.
    :return: HTML response with the learn page content for logged-in user.
    """
    return templates.TemplateResponse(
        request=request,
        name="learn.html",
        context={
            "_": _(language.value),
            "language": language.value,
            "username": current_user.username,
        },
    )


@router.get("/page_not_found")
async def page_not_found(
    request: Request, language: LanguageModel = LanguageModel.ru
) -> HTMLResponse:
    """
    Serve the error page with a custom image based on the status code and language.

    :param request: HTTP request.
    :param language: Language code.
    :return: HTML response with the error page.
    """
    return templates.TemplateResponse(
        request=request,
        name="page_not_found.html",
        context={"_": _(language.value), "language": language.value},
    )


@router.get("/favorites")
async def get_favorite_words(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    current_user: UserBase = Depends(get_current_user),
) -> HTMLResponse:
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
            "_": _(language.value),
            "language": language.value,
            "username": current_user.username,
            "user_id": current_user.user_id,
        },
    )


@router.get("/tests")
async def get_tests_page(
    request: Request,
    language: LanguageModel = LanguageModel.ru,
    current_user: UserBase = Depends(get_current_user),
) -> HTMLResponse:
    """
    Serve the tests page.

    :param request: HTTP request.
    :param language: Language code.
    :param current_user: Current user dependency.
    :return: HTML response with the tests page.
    """
    return templates.TemplateResponse(
        request=request,
        name="tests.html",
        context={
            "_": _(language.value),
            "language": language.value,
            "username": current_user.username,
        },
    )
