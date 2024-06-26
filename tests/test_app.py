import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


@pytest.fixture(scope="module")
def test_client():
    BaseModel.metadata.create_all(bind=engine)
    yield TestClient(app)
    BaseModel.metadata.drop_all(bind=engine)
