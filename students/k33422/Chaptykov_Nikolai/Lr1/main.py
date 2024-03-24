from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from connection import *
from routes import router
import uvicorn


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
alembic revision --autogenerate -m "skill added"
alembic upgrade head
"""