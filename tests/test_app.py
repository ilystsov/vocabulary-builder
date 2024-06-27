import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vocabulary_builder.db.crud import get_user_by_username
from vocabulary_builder.db.database import BaseModel
from vocabulary_builder.main import app, get_db


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client():
    BaseModel.metadata.create_all(bind=engine)
    yield TestClient(app)
    BaseModel.metadata.drop_all(bind=engine)


def test_register_user(test_client, db_session):
    response = test_client.post(
        "/signup", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    user = get_user_by_username(db_session, "testuser")
    assert user is not None


def test_login_user(test_client):
    test_client.post(
        "/signup", data={"username": "testuser", "password": "testpassword"}
    )
    response = test_client.post(
        "/login", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200


def test_get_main_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "html" in response.text


def test_get_new_word(test_client):
    response = test_client.get("/new_word?language=ru")
    assert response.status_code == 200
    assert "word" in response.json() or response.json() == {"message": "No word found"}


def test_learn_endpoint(test_client):
    test_client.post(
        "/signup", data={"username": "testuser", "password": "testpassword"}
    )
    login_response = test_client.post(
        "/login", data={"username": "testuser", "password": "testpassword"}
    )
    cookies = login_response.cookies
    for cookie in cookies:
        test_client.cookies.set(cookie.name, cookie.value)

    response = test_client.get("/learn?language=ru")
    assert response.status_code == 200
