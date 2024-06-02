from fastapi import FastAPI
from db.connection import init_db, get_session
from endpoints.user_endpoints import user_router
from endpoints.author_endpoints import author_router
from endpoints.book_endpoints import book_router
from endpoints.book_instance_endpoints import book_instance_router
from endpoints.book_exchange_endpoints import book_exchange_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_session()
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(author_router, prefix="/api/authors", tags=["authors"])
app.include_router(book_router, prefix="/api/books", tags=["books"])
app.include_router(book_instance_router, prefix="/api/instances", tags=["instances"])
app.include_router(book_exchange_router, prefix="/api/exchanges", tags=["exchanges"])
