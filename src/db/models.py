from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import BaseModel


class WordModel(BaseModel):
    __tablename__ = 'words'
    id: Mapped[UUID] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(nullable=False)
    translated_word: Mapped[str] = mapped_column(nullable=False)
    context: Mapped[str] = mapped_column(nullable=False)
    translated_context: Mapped[str] = mapped_column(nullable=False)
