from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine(
    url="sqlite:///bookmarkmanager.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    """Creates the tables in the database."""

    from app.models.bookmarks import Bookmark  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Gets SQLAlchemy Session for interacting with the database."""

    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
