from typing_extensions import TypedDict
from fastapi import FastAPI

from model import Profile, Book, Account

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"

@app.get("/accounts_list")
def accounts_list() -> list[Account]:
    return temp_bd

@app.get("/account/{account_id}")
def accounts_list(account_id: int) -> list[Account]:
    return [account for account in temp_bd if account.get("id") == account_id]

@app.post("/account")
def accounts_create(account: Account) -> TypedDict('Response', {"status": int, "data": Account}): # type: ignore
    account_to_append = account.model_dump()
    temp_bd.append(account_to_append)
    return {"status": 200, "data": account}

@app.delete("/account/delete/{account_id}")
def account_delete(account_id: int) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    for i, account_from_dict in enumerate(temp_bd):
        if account_from_dict.get("id") == account_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}

@app.put("/account/{account_id}")
def account_update(account_id: int, account: Account) -> list[Account]:
    for i, war in enumerate(temp_bd):
        if war.get("id") == account_id:
            temp_bd[i] = account
    return temp_bd


temp_bd = [{
    "id": 1,
    "login": "inko",
    "password": "qwerty",
    "email": "inko@lun.ver",
    "profile": {
        "id": 1,
        "full_name": "Инко Лунберг",
        "city": "Дауд",
        "about": "Искусный дипломат"
    },
    "books": [
        {
            "id": 1,
            "title": "Стража! Стража!",
            "author": "Терри Пратчетт",
            "year": 989,
            "condition": "good",
            "genre": "Научная фантастика",
            "language": "Русский",
            "description": "Ваймс крут!",
            "status": "reserved"
        },
        {
            "id": 2,
            "title": "К оружию! К оружию!",
            "author": "Терри Пратчетт",
            "year": 993,
            "condition": "good",
            "genre": "Научная фантастика",
            "language": "Русский",
            "description": "Ваймс ещё круче!",
            "status": "available"
        },
    ]
},
    {
        "id": 2,
        "login": "lessa",
        "password": "qwerty",
        "email": "lessa@lun.ver",
        "profile": {
            "id": 2,
            "full_name": "Лессандра Виннар",
            "city": "Дауд",
            "about": "Авантюрист, хирург и просто хорошая девочка"
        },
        "books": []
    },
]


@app.get("/books_list")
def books_list() -> list[Book]:
    return book_db

@app.get("/book/{book_id}")
def books_list(book_id: int) -> list[Book]:
    return [book for book in book_db if book.get("id") == book_id]

@app.post("/book")
def books_create(book: Book) -> TypedDict('Response', {"status": int, "data": Book}): # type: ignore
    book_to_append = book.model_dump()
    book_db.append(book_to_append)
    return {"status": 200, "data": book}

@app.delete("/book/delete/{book_id}")
def book_delete(book_id: int) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    for i, book_from_dict in enumerate(book_db):
        if book_from_dict.get("id") == book_id:
            book_db.pop(i)
            break
    return {"status": 201, "message": "deleted"}

@app.put("/book/{book_id}")
def book_update(book_id: int, book: Book) -> list[Book]:
    for i, war in enumerate(book_db):
        if war.get("id") == book_id:
            book_db[i] = book
    return book_db

book_db = [
        {
            "id": 1,
            "title": "Стража! Стража!",
            "author": "Терри Пратчетт",
            "year": 989,
            "condition": "good",
            "genre": "Научная фантастика",
            "language": "Русский",
            "description": "Ваймс крут!",
            "status": "reserved"
        },
        {
            "id": 2,
            "title": "К оружию! К оружию!",
            "author": "Терри Пратчетт",
            "year": 993,
            "condition": "good",
            "genre": "Научная фантастика",
            "language": "Русский",
            "description": "Ваймс ещё круче!",
            "status": "available"
        },
    ]