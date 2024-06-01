from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import WordModel


def get_random_word(db: Session):
    stmt = select(WordModel).order_by(func.random()).limit(1)
    random_row = db.scalars(stmt).first()
    return random_row
