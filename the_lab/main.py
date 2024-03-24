from fastapi import FastAPI, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List

# from models import
from connection import init_db, get_session

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"
