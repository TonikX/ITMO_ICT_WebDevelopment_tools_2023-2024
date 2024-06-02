import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from endpoints.user import user_router
from endpoints.finance import main_router

app = FastAPI()

app.include_router(user_router)
app.include_router(main_router, prefix="/api")


def create_db():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db()


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001, reload=True)