from fastapi import FastAPI
import uvicorn
from database.conn import init_db
from endpoints.author import author_router
from endpoints.book import book_router
from endpoints.bookexchange import book_exchange_router
from endpoints.bookinstance import book_instance_router
from endpoints.user import user_router
from endpoints.parser import parser_router


app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(author_router, prefix="/api/authors", tags=["authors"])
app.include_router(book_router, prefix="/api/books", tags=["books"])
app.include_router(book_instance_router, prefix="/api/instances", tags=["instances"])
app.include_router(book_exchange_router, prefix="/api/exchanges", tags=["exchanges"])
app.include_router(parser_router, prefix="/api/parser", tags=["parser"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8001, reload=True)
