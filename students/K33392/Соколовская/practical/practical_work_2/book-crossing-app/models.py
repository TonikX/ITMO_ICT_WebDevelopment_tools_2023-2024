from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from typing import List, Optional
import datetime


class CategoryDefault(SQLModel):
    name: str


class BookCategory(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)


class Category(CategoryDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    books: Optional[List["Book"]] = Relationship(back_populates="categories", link_model=BookCategory)


class AuthorDefault(SQLModel):
    name: str


class Author(AuthorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    books: Optional[List["Book"]] = Relationship(back_populates="author")


class BookDefault(SQLModel):
    name: str
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")


class Book(BookDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    author: Optional[Author] = Relationship(back_populates="books")
    categories: Optional[List[Category]] = Relationship(back_populates="books", link_model=BookCategory)


class BookOut(BookDefault):
    id: int
    author: Optional[Author] = None
    categories: Optional[List[Category]] = None


class BookIn(BookDefault):
    pass

# class BookAuthor(BookDefault):
#     author:
