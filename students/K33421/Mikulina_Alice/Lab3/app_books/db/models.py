from enum import Enum
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel


class AppUserDefault(SQLModel):
    username: str
    email: str
    password: str
    about: Optional[str] = None
    location: Optional[str] = None

class AppUser(AppUserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    is_admin: Optional[bool] = Field(default=False)
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)



class BookGenreDefault(SQLModel):
    book_id: int = Field(foreign_key="book.id")
    genre_id: int = Field(foreign_key="genre.id")

class BookGenre(BookGenreDefault, table=True):
    id: int = Field(default=None, primary_key=True)



class GenreDefault(SQLModel):
    name: str

class Genre(GenreDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    books: Optional[List["Book"]] = Relationship(
        back_populates="genres",
        link_model=BookGenre
    )



class BookDefault(SQLModel):
    title: str
    author: str
    description: Optional[str] = None
    condition: str

class Book(BookDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="appuser.id")
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)
    genres: Optional[List[Genre]] = Relationship(
        back_populates="books",
        link_model=BookGenre
    )



class StatusType(Enum):
    pending = "pending"
    declined = "declined"
    approved = "approved"
    exchanged = "exchanged"

class RequestDefault(SQLModel):
    requester_book_id: int = Field(foreign_key="book.id")
    recipient_book_id: int = Field(foreign_key="book.id")
    message: str
    status: StatusType

class Request(RequestDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)
    new_field: Optional[str]