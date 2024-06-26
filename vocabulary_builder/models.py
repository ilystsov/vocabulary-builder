from pydantic import UUID4, BaseModel


class UserBase(BaseModel):
    user_id: str
    username: str


class WordBase(BaseModel):
    word_id: UUID4
