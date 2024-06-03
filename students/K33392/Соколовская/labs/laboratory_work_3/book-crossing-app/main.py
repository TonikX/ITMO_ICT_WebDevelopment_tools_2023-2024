from fastapi import FastAPI

from connection import init_db
from controller import author, book, category, user, sharing, book_copy, parser

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app = FastAPI()
app.include_router(author.router)
app.include_router(parser.router)
app.include_router(category.router)
app.include_router(book.router)
app.include_router(user.router)
app.include_router(book_copy.router)
app.include_router(sharing.router)
