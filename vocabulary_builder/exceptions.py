"""Custom exceptions for the application."""
from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """Exception raised for invalid credentials."""

    def __init__(self) -> None:
        """Initialize the CredentialsException."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class IncorrectUsernamePasswordException(HTTPException):
    """Exception raised for incorrect username or password."""

    def __init__(self) -> None:
        """Initialize the IncorrectUsernamePasswordException."""
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class WordNotFound(Exception):
    """Exception raised when a word is not found."""


class UserNotFound(Exception):
    """Exception raised when a user is not found."""


class BadIdentifier(Exception):
    """Exception raised for a bad identifier."""
