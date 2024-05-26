from fastapi import APIRouter

from src.web_api.routes import users, books, exchange_requests

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(
    exchange_requests.router, prefix="/exchange_requests", tags=["exchange_requests"]
)
