from typing_extensions import TypedDict

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select

from connection import init_db, get_session
from db.models import *

# Importing put endpoints
from endpoints.users import router as users_router
from endpoints.books import router as books_router
from endpoints.genres import router as genres_router
from endpoints.book_genre import router as book_genre_router
from endpoints.requests import router as requests_router
from endpoints.auth import router as auth_router

app = FastAPI()

# Mounting our endpoints
app.include_router(auth_router, prefix="", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(genres_router, prefix="/genres", tags=["genres"])
app.include_router(book_genre_router, prefix="/bookgenre", tags=["bookgenre"])
app.include_router(requests_router, prefix="/requests", tags=["requests"])


@app.get("/")
def hello():
    return "Hello, [username]!"


if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="localhost", port=8000)
