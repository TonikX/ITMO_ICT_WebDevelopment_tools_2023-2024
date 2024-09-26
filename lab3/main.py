from fastapi import FastAPI
from routes import notification
from routes import budget, auth, transactioncategory, parser, user, category, \
    transaction, goal

from connection import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(parser.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(goal.router)
app.include_router(budget.router)
app.include_router(category.router)
app.include_router(transaction.router)
app.include_router(notification.router)
app.include_router(transactioncategory.router)