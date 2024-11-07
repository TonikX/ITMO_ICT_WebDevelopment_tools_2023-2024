from fastapi import FastAPI
from typing import List
from typing_extensions import TypedDict

from models import Book, Library, Request

app = FastAPI()

temp_bd = [{
    "book_id": 1,
    "book_name": "Собака Баскервилей",
    "book_author": "Артур Конан Дойл",
    "book_condition": "отличное",
    "library": {
        "library_id": 1,
        "user_id": 1,
        "library_name": "Библиотека классики"
        },
    "requests":[{
        "request_id": 1,
        "user_id": 2,
        "request_date": "2024-09-13 10:00",
        "request_status": "ожидание"
        },
        {
        "request_id": 2,
        "user_id": 3,
        "request_date": "2024-09-13 08:00",
        "request_status": "ожидание"
        }]
    },
    {
    "book_id": 2,
    "book_name": "Мрачный Жнец",
    "book_author": "Терри Пратчетт",
    "book_condition": "хорошее",
    "library": {
        "library_id": 2,
        "user_id": 2,
        "library_name": "Моя библиотека"
        },
    "requests":[{
        "request_id": 3,
        "user_id": 1,
        "request_date": "2024-09-13 11:00:00",
        "request_status": "одобрено"
        },
        {
        "request_id": 4,
        "user_id": 3,
        "request_date": "2024-09-13 18:00:00",
        "request_status": "отклонено"
        }]
    }
]

# API для книг

@app.get("/books_list")
def books_list() -> List[Book]:
    return temp_bd

@app.get("/book/{id_book}")
def book_get(id_book: int)-> List[Book]:
    return [book for book in temp_bd if book.get("book_id") == id_book]

@app.post("/book")
def book_create(book: Book) -> TypedDict('Response', {"status": int, "data": Book}):
    book_to_append = book.model_dump()
    temp_bd.append(book_to_append)
    return {"status": 200, "data": book}

@app.delete("/book/delete{id_book}")
def book_delete(id_book: int):
    for i, book in enumerate(temp_bd):
        if book.get("book_id") == id_book:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}

@app.put("/book{id_book}")
def book_update(id_book: int, book: Book) -> List[Book]:
    for bo in temp_bd:
        if bo.get("book_id") == id_book:
            book_to_append = book.model_dump()
            temp_bd.remove(bo)
            temp_bd.append(book_to_append)
    return temp_bd

# API для библиотек (вложенного объекта)

@app.get("/libraries_list")
def libraries_list() -> List[Library]:
    libs = [book.get("library") for book in temp_bd]
    lib_ids = list(set([lib.get("library_id") for lib in libs]))
    libraries = []
    for lib in libs:
        if lib.get("library_id") in lib_ids:
            libraries.append(lib)
            lib_ids.remove(lib.get("library_id"))
        continue     
    return libraries

@app.get("/library/{id_library}")
def library_get(id_library: int)-> Library:
    return [book.get("library") for book in temp_bd if book.get("library").get("library_id") == id_library][0]

@app.post("/library")
def library_create(library: Library) -> TypedDict('Response', {"status": int, "data": Library}):
    id_book = max([book.get("book_id") for book in temp_bd]) + 1
    library_to_append = library.model_dump()
    book_to_append = {
    "book_id": id_book,
    "book_name": "bookname",
    "book_author": "author",
    "book_condition": "хорошее",
    "library": library_to_append,
    "requests":[]
    }
    temp_bd.append(book_to_append)
    return {"status": 200, "data": library}

@app.delete("/library/delete{id_library}")
def library_delete(id_library: int):
    for book in reversed(temp_bd):
        if book.get("library").get("library_id") == id_library:
            temp_bd.remove(book)
    return {"status": 201, "message": "deleted"}

@app.put("/library{id_library}")
def library_update(id_library: int, library: Library) -> List[Library]:
    books_updated = []
    for book in reversed(temp_bd):
        if book.get("library").get("library_id") == id_library:
            library_to_append = library.model_dump()
            book_to_append = {
            "book_id": book.get("book_id"),
            "book_name": book.get("book_name"),
            "book_author": book.get("book_author"),
            "book_condition": book.get("book_condition"),
            "library": library_to_append,
            "requests":book.get("requests")
            }
            books_updated.append(book_to_append)
            temp_bd.remove(book)
    temp_bd.extend(books_updated)

    #вывод всех библиотек
    libs = [book.get("library") for book in temp_bd]
    lib_ids = list(set([lib.get("library_id") for lib in libs]))
    libraries = []
    for lib in libs:
        if lib.get("library_id") in lib_ids:
            libraries.append(lib)
            lib_ids.remove(lib.get("library_id"))
        continue     
    return libraries