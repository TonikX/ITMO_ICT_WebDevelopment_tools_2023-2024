from fastapi import FastAPI

from db import *
from routers import customers, categories, operations, transactions

app = FastAPI()  # создаем приложение

app.include_router(customers.customerRouter)  # включаем роутер пользователей
app.include_router(categories.categoryRouter)  # включаем роутер категорий
app.include_router(operations.operationRouter)  # включаем роутер операций
app.include_router(transactions.transactionRouter)  # включаем роутер транзакций


@app.on_event("startup")  # при событии запуска сервера выполняется эта функция
def on_startup():
    init_db()  # вызов функции из файла db.py
