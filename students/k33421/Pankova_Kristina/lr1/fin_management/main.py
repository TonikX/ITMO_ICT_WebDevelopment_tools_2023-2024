from typing import List, Optional
from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.models import *
from models.user_models import *
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select
from endpoints.user_endpoints import user_router

from db.connection import *
from typing_extensions import TypedDict
app = FastAPI()
app.include_router(user_router)


@app.get("/")
def hello():
    return "Hello, [username]!"


# User API endpoints
@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/user/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    try:
        user = session.get(User, user_id)
        return user
    except NoResultFound:
        return {"message": "User not found"}

@app.post("/user")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Category API endpoints
