from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from src.db.crud import get_random_word
from src.db.database import SessionLocal

app = FastAPI()

def get_db():
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


@app.get('/', response_class=HTMLResponse)
def get_main_page(request: Request, db: Session = Depends(get_db)):
    random_row = get_random_word(db)
    context = {
        'word': random_row.word,
        'translated_word': random_row.translated_word,
        'context': random_row.context,
        'translated_context': random_row.translated_context,
    }

    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context=context,
    )
