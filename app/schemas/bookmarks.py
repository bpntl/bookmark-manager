from datetime import datetime

from pydantic import BaseModel, Field

from app.models.bookmarks import BookmarkStatus, BookmarkType


class BaseBookmark(BaseModel):
    name: str
    address: str
    description: str
    type: BookmarkType


class BookmarkRead(BaseBookmark):
    id: int
    status: BookmarkStatus
    date_added: datetime
    date_modified: datetime


class BookmarkCreate(BaseBookmark):
    pass


class BookmarkUpdate(BaseModel):
    name: str | None = Field(default=None)
    address: str | None = Field(default=None)
    description: str | None = Field(default=None)
    type: BookmarkType | None = Field(default=None)
    status: BookmarkStatus | None = Field(default=None)
