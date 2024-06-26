from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class SaveWord(BaseModel):
    user_id: UUID
    word_id: UUID
