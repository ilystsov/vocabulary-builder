from pydantic import UUID4, BaseModel


class UserBase(BaseModel):
    """
    Base model for user data.

    :param user_id: ID of the user.
    :param username: Username of the user.
    """

    user_id: str
    username: str


class WordBase(BaseModel):
    """
    Base model for word data.

    :param word_id: ID of the word.
    """

    word_id: UUID4
