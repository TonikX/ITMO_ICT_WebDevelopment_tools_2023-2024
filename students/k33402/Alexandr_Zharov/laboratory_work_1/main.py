import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from db.db import engine
from endpoints.user_endpoints import user_router
from models.user_models import *

app = FastAPI()

app.include_router(user_router)

def creacte_db():
    SQLModel.metadata.create_all(engine)

@app.get('/')
def hello():
    return 'Hello world'

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
    creacte_db()