from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    username: str


class SaveWord(BaseModel):
    user_id: str
    word_id: str
