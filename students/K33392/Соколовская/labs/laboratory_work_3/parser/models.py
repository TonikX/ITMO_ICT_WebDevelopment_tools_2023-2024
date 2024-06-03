from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from typing import List, Optional
import datetime


class BookCategory(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    books: Optional[List["Book"]] = Relationship(back_populates="categories", link_model=BookCategory)


class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    books: Optional[List["Book"]] = Relationship(back_populates="author")


class BookCopy(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")
    author: Optional[Author] = Relationship(back_populates="books")
    categories: Optional[List[Category]] = Relationship(back_populates="books", link_model=BookCategory)
    owners: Optional[List["User"]] = Relationship(back_populates="own_books", link_model=BookCopy)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    own_books: Optional[List[Book]] = Relationship(back_populates="owners", link_model=BookCopy)
    shared_books: Optional[List["Sharing"]] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs=dict(foreign_keys="[Sharing.owner_id]")
    )
    borrowed_books: Optional[List["Sharing"]] = Relationship(
        back_populates="taking",
        sa_relationship_kwargs=dict(foreign_keys="[Sharing.taking_id]")
    )


class SharingStatus(Enum):
    requested = "requested"
    active = "active"
    archived = "archived"


class Sharing(SQLModel, table=True):
    owner_id: int = Field(foreign_key="user.id")
    taking_id: int = Field(foreign_key="user.id")
    book_copy_id: int = Field(foreign_key="bookcopy.id")
    id: int = Field(default=None, primary_key=True)
    owner: Optional["User"] = Relationship(back_populates="shared_books",
                                           sa_relationship_kwargs=dict(foreign_keys="[Sharing.owner_id]")
                                           )
    taking: Optional["User"] = Relationship(back_populates="borrowed_books",
                                            sa_relationship_kwargs=dict(foreign_keys="[Sharing.taking_id]")
                                            )

    status: SharingStatus = Field(default=SharingStatus.requested)


class CategoryIn(SQLModel):
    name: str


class CategoryOut(CategoryIn):
    id: int
    books: Optional[List["Book"]] = None


class AuthorIn(SQLModel):
    name: str


class AuthorOut(AuthorIn):
    id: int
    books: Optional[List["Book"]] = None


class BookIn(SQLModel):
    name: str
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")


class BookOut(BookIn):
    id: int
    author: Optional[Author] = None
    categories: Optional[List[Category]] = None
    owners: Optional[List[User]] = None


class UserIn(SQLModel):
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserPassword(SQLModel):
    password: str


class UserOut(UserIn):
    id: int
    own_books: Optional[List[Book]] = None
    shared_books: Optional[List["Sharing"]] = None
    borrowed_books: Optional[List["Sharing"]] = None
