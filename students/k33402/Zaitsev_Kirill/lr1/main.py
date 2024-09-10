from fastapi import FastAPI
from router import customers, categories, operations, transactions
from db import init_db

app = FastAPI()

app.include_router(customers.customerRouter)
app.include_router(categories.categoryRouter)
app.include_router(operations.operationRouter)
app.include_router(transactions.transactionRouter)


@app.on_event("startup")
def on_startup():
    init_db()
