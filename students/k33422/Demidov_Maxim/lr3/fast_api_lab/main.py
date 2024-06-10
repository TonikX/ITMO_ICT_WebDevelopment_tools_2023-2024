from fastapi import FastAPI

from db import init_db
from endpoints.users import users_router
from endpoints.team import team_router
from endpoints.parser import parser_router

app = FastAPI()

app.include_router(users_router)
app.include_router(team_router)
app.include_router(parser_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello():
    return "Hello there"
