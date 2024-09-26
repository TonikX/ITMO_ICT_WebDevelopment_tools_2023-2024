from fastapi import FastAPI, Depends, HTTPException
from typing_extensions import TypedDict
from typing import List
from sqlmodel import select
from fastapi import FastAPI
from routes import user, goal, budget, category, transaction, notification, transactioncategory, auth

from connection import init_db, get_session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(goal.router)
app.include_router(budget.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(notification.router)
app.include_router(transactioncategory.router)