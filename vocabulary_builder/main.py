"""Main application file for Vocabulary Builder."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from vocabulary_builder.routes import auth, pages, users, words


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)


app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(users.router)
app.include_router(words.router)


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
    response = RedirectResponse(url="/page_not_found", status_code=303)
    return response
