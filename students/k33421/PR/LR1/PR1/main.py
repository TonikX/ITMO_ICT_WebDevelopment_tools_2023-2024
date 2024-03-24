from enum import Enum
from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


temp_bd = [{  "id": 1,
              "title": "Hello",
              "author": "Greeting G.B.",
              "genre": "poetry",
              "publisher": "publisher agency 1",
              "year_of_publication": 2000,
              "description": "hello and goodby book",
              "owner_id": {
                  "id": 1,
                  "username": "arina12345",
                  "hashed_password": "arina12345",
                  "name": "Arina",
                  "surname": "Belova",
                  "email": "arinbel@mail.ru",
                  "country": "Russia",
                  "city": "Moscow"
              }},
           {"id": 2,
            "title": "Horror",
            "author": "Black C.B.",
            "genre": "horror",
            "publisher": "publisher agency 2",
            "year_of_publication": 2001,
            "description": "dark story",
            "owner_id": {
                "id": 2,
                "username": "anna12345",
                "hashed_password": "anna12345",
                "name": "Anna",
                "surname": "Annova",
                "email": "anna@mail.ru",
                "country": "Russia",
                "city": "Moscow"
            }},
            { "id": 3,
              "title": "My poetry",
              "author": "Pushkin A.S.",
              "genre": "poetry",
              "publisher": "publisher agency 1",
              "year_of_publication": 1990,
              "description": "fantastic poetry",
              "owner_id": {
                  "id": 1,
                  "username": "arina12345",
                  "hashed_password": "arina12345",
                  "name": "Arina",
                  "surname": "Belova",
                  "email": "arinbel@mail.ru",
                  "country": "Russia",
                  "city": "Moscow"
              }}
           ]


class Genres(Enum):
    fantasy = "fantasy"
    detectives = "detectives"
    romance = "romance"
    thrillers = "thrillers"
    horrors = "horrors"
    comics = "comics"
    adventures = "adventures"
    poetry = "poetry"
    other = "other"


class Books(BaseModel):
    title: str
    author: str
    genre: Genres
    publisher: str
    year_of_publication: int
    description: str


class Users(BaseModel):
    name: str
    surname: str
    email: str
    country: str
    city: str
    books: List[Books] = []


@app.get("/")
def hello():
    return "Hello, Diana!"


@app.get("/books_list")
def books_list() -> List[Books]:
    return temp_bd


@app.get("/books/{books_id}")
def books_get(books_id: int) -> List[Books]:
    return [books for books in temp_bd if books.get("id") == books_id]


@app.post("/books")
def books_create(books: Books):
    books_to_append = books.model_dump()
    temp_bd.append(books_to_append)
    return {"status": 200, "data": books}


@app.delete("/books/delete{books_id}")
def books_delete(books_id: int):
    for i, books in enumerate(temp_bd):
        if books.get("id") == books_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/books{books_id}")
def books_update(books_id: int, books: Books) -> List[Books]:
    for bok in temp_bd:
        if bok.get("id") == books_id:
            books_to_append = books.model_dump()
            temp_bd.remove(bok)
            temp_bd.append(books_to_append)
    return temp_bd

