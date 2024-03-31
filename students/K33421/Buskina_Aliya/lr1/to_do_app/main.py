from fastapi import FastAPI
from connection import *
import routes

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("Initializing database...")
    init_db()
    print("Database initialized.")

app.include_router(routes.router)
