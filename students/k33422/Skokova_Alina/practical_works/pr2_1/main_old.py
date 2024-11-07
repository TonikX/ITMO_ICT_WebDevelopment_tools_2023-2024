from fastapi import FastAPI

app = FastAPI()

temp_bd = [{
    "book_id": 1,
    "book_name": "Собака Баскервилей",
    "book_author": "Артур Конан Дойл",
    "book_condition": "отличное",
    "library_id": {
        "library_id": 1,
        "user_id": 1,
        "library_name": "Библиотека классики"
        },
    },
    {
    "book_id": 2,
    "book_name": "Мрачный Жнец",
    "book_author": "Терри Пратчетт",
    "book_condition": "хорошее",
    "library_id": {
        "library_id": 2,
        "user_id": 2,
        "library_name": "Моя библиотека"
        },
    },
]

@app.get("/")
def hello():
    return "Hello, Compukter!"

@app.get("/books_list")
def books_list():
    return temp_bd

@app.get("/book/{id_book}")
def book_get(id_book: int):
    return [book for book in temp_bd if book.get("book_id") == id_book]

@app.post("/book")
def book_add(book: dict):
    temp_bd.append(book)
    return {"status": 200, "data": book}

@app.delete("/book/delete{id_book}")
def book_delete(id_book: int):
    for i, book in enumerate(temp_bd):
        if book.get("book_id") == id_book:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}

@app.put("/book{id_book}")
def book_update(id_book: int, book: dict):
    for i, bo in enumerate(temp_bd):
        if bo.get("book_id") == id_book:
            temp_bd[i] = book
    return temp_bd