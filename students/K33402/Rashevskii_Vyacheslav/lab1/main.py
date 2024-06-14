from fastapi import FastAPI

from db import *
from routers import categories, customers, operations, transactions

# https://rendex85.github.io/WebDevelopmentLabsDocs/lr2/lr2/

app = FastAPI()
app.include_router(customers.customerRouter)
app.include_router(categories.categoryRouter)
app.include_router(operations.operationRouter)
app.include_router(transactions.transactionRouter)


@app.on_event("startup")
def on_startup():
    init_db()

# TODO add find by aliases
