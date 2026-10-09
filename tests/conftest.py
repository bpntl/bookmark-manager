from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.db.session import get_session
from app.main import app
from app.models.bookmarks import Bookmark  # noqa: F401

TEST_DATABASE_URL = "sqlite:///testbookmarks.db"

engine = create_engine(
    url=TEST_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLModel.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session]:
    """Creates a new database session with a rollback at the end of the test."""

    with Session(bind=engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_client(db_session) -> Generator[TestClient]:
    """Creates a test client that overrides with a fixture to return a session."""

    def override_get_session():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client
