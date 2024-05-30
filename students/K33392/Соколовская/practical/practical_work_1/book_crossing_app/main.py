from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing_extensions import TypedDict

app = FastAPI()


temp_bd = {
    "books": [
        {
            "id": 1,
            "name": "Мастер и Маргарита",
            "author_id": 1,
            "categorys": [
                {"id": 1, "name": "Роман"},
                {"id": 2, "name": "Мистика"},
            ],
        },
        {
            "id": 2,
            "name": "Отцы и дети",
            "author_id": 2,
            "categorys": [
                {"id": 1, "name": "Роман"},
            ],
        },
    ],
    "authors": [
        {"id": 1, "name": "Булгаков М. А."},
        {"id": 2, "name": "Тургенев И. С."},
    ],
}


class Author(BaseModel):
    id: int
    name: str


class Category(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    id: int
    name: str
    Author_id: int
    categories: Optional[list[Category]] = []


@app.get("/books")
def books_list() -> list[Book]:
    return temp_bd["books"]


@app.get("/books/{book_id}")
def books_get(book_id: int) -> list[Book]:
    return [book for book in temp_bd["books"] if book.get("id") == book_id]


@app.post("/books")
def books_create(book: Book) -> Book:
    temp_bd["books"].append(book.dict())
    return book


@app.delete("/books/{book_id}")
def Book_delete(book_id: int) -> TypedDict("Response", {"message": str}):
    for i, book in enumerate(temp_bd["books"]):
        if book.get("id") == book_id:
            temp_bd["books"].pop(i)
            break
    return temp_bd


@app.put("/books/{book_id}")
def book_update(book_id: int, book: dict) -> Book:
    for i, cur in enumerate(temp_bd["books"]):
        if cur.get("id") == book_id:
            temp_bd["books"][i] = book
    return temp_bd


@app.get("/authors")
def get_authors() -> list[Author]:
    return temp_bd["authors"]


@app.get("/authors/{author_id}")
def get_author(author_id: int) -> Author:
    for author in temp_bd["authors"]:
        if author["id"] == author_id:
            return author
    raise HTTPException(status_code=404, detail="Author not found")


@app.post("/authors")
def create_author(author: Author) -> Author:
    temp_bd["authors"].append(author.dict())
    return temp_bd


@app.put("/authors/{author_id}")
def update_author(author_id: int, author: Author) -> Author:
    for auth in temp_bd["authors"]:
        if auth["id"] == author_id:
            auth.update(Author.dict())
            return author
    raise HTTPException(status_code=404, detail="Author not found")


@app.delete("/authors/{author_id}")
def delete_author(author_id: int) -> TypedDict("Response", {"message": str}):
    for i, author in enumerate(temp_bd["authors"]):
        if author["id"] == author_id:
            temp_bd["authors"].pop(i)
            return {"message": "Author deleted successfully"}
    raise HTTPException(status_code=404, detail="Author not found")


@app.get("/")
def hello():
    return "Hello, world!"


