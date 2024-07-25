import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.requests import Request

from vocabulary_builder.db.crud import get_user_by_username
from vocabulary_builder.dependencies import get_db
from vocabulary_builder.exceptions import CredentialsException
from vocabulary_builder.models import UserBase


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """Custom OAuth2 password bearer class that supports cookies."""

    async def __call__(self, request: Request) -> str:
        """
        Retrieve the access token from the request cookies.

        :param request: HTTP request.
        :return: Access token.
        :raises HTTPException: If the access token is not found in cookies.
        """
        authorization: str = request.cookies.get("access_token")
        if not authorization:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return authorization


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")


def get_hashed_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    :param password: Plain text password.
    :return: Hashed password.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    :param plain_password: Plain text password.
    :param hashed_password: Hashed password.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
) -> UserBase | bool:
    """
    Authenticate a user by username and password.

    :param username: Username.
    :param password: Password.
    :param db: Database session dependency.
    :return: User representation if authentication is successful, False otherwise.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return UserBase(username=username, user_id=str(user.id))


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT access token.

    :param data: Data to encode in the token.
    :param expires_delta: Token expiration time.
    :return: Encoded JWT token.
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserBase:
    """
    Get the current user based on the JWT token.

    :param token: JWT token.
    :param db: Database session dependency.
    :return: Current user.
    """
    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if username is None or user_id is None:
            raise CredentialsException
    except InvalidTokenError:
        raise CredentialsException
    user = get_user_by_username(db, username)
    if user is None:
        raise CredentialsException
    return UserBase(username=username, user_id=user_id)
