from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class BookmarkStatus(str, Enum):
    added = "added"
    viewed = "viewed"
    archived = "archived"


class BookmarkType(str, Enum):
    article = "article"
    website = "website"
    blog = "blog"
    post = "post"
    forum = "forum"
    wiki = "wiki"
    portfolio = "portfolio"
    documentation = "documentation"
    file = "file"
    image = "image"
    audio = "audio"
    video = "video"
    gif = "gif"


class Bookmark(SQLModel, table=True):
    """SQLModel for bookmarks table."""

    __tablename__ = "bookmark" # type: ignore

    id: int = Field(default=None, primary_key=True)
    name: str
    address: str
    description: str
    type: BookmarkType
    status: BookmarkStatus
    date_added: datetime
    date_modified: datetime
