from fastapi import FastAPI

from personal_finance.infrastructure.persistance.postgres.database import init_db
from personal_finance.presentation.http.router import app_router

app = FastAPI()

app.include_router(app_router)


@app.on_event('startup')
def startup():
    init_db()
    print("Database initialized")

