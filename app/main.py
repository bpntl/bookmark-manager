from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query, status
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import select

from app.db.session import SessionDep, create_db_tables
from app.models.bookmarks import Bookmark, BookmarkStatus
from app.schemas.bookmarks import BookmarkCreate, BookmarkRead, BookmarkUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    """Handles the actions on application startup and shutdown."""

    print(panel.Panel("Server started", border_style="green"))
    
    create_db_tables()

    yield

    print(panel.Panel("Server stopped", border_style="red"))


app = FastAPI(lifespan=lifespan_handler,)


@app.get("/bookmarks", response_model=list[BookmarkRead])
def get_bookmarks(session: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)):
    """Gets a list of all the bookmarks."""

    bookmarks = session.exec(select(Bookmark).offset(offset).limit(limit)).all()

    return bookmarks


@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkRead)
def get_bookmark(session: SessionDep, bookmark_id: int):
    """Gets a bookmark based on the given id."""

    bookmark = session.get(Bookmark, bookmark_id)

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark with the given id doesn't exist."
        )

    return bookmark


@app.post("/bookmarks", response_model=BookmarkRead)
def create_bookmark(session: SessionDep, bookmark: BookmarkCreate):
    """Creates a new bookmark."""

    current_timestamp = datetime.now() # noqa: DTZ005
    new_bookmark = Bookmark(
        **bookmark.model_dump(),
        status=BookmarkStatus.added,
        date_added=current_timestamp,
        date_modified=current_timestamp,
    )

    session.add(new_bookmark)
    session.commit()
    session.refresh(new_bookmark)

    return new_bookmark


@app.patch("/bookmarks/{bookmark_id}", response_model=BookmarkRead)
def update_bookmark(session: SessionDep, bookmark_id: int, bookmark_update: BookmarkUpdate):
    """Updates an existing bookmark's specified fields."""

    bookmark = session.get(Bookmark, bookmark_id)

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark with the given id doesn't exist",
        )

    bookmark_update_data = bookmark_update.model_dump(exclude_unset=True)
    bookmark_update_data.update({"date_modified": datetime.now()})  # noqa: DTZ005

    bookmark.sqlmodel_update(bookmark_update_data)

    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)

    return bookmark


@app.delete("/bookmarks/{bookmark_id}")
def delete_bookmark(session: SessionDep, bookmark_id: int) -> dict[str, str]:
    """Deletes the specified bookmark from the database."""

    bookmark = session.get(Bookmark, bookmark_id)
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark with the given id doesn't exist",
        )

    session.delete(bookmark)
    session.commit()

    return {"detail": f"Bookmark with id #{bookmark_id} was deleted."}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    """Gets Scalar API Documentation."""

    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
