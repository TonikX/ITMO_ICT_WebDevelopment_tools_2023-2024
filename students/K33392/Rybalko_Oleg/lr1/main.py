from contextlib import asynccontextmanager

from fastapi import FastAPI

from conn import init_db
from routers import (auth_router, budgets_in_categories_router, budgets_router, categories_router, transactions_router,
                     users_router)


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=app_lifespan)
app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(budgets_router)
app.include_router(categories_router)
app.include_router(budgets_in_categories_router)
app.include_router(auth_router)
