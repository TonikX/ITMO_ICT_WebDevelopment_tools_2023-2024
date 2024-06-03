from fastapi import APIRouter
from . import root, balances, transactions, categories, users, articles

api_router = APIRouter()

api_router.include_router(root.router, prefix="", tags=["root"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(balances.router, prefix="/balances")
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
