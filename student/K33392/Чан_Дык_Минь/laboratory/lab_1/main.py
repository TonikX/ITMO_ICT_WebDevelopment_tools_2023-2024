from connection import init_db, get_session
from fastapi import FastAPI, Depends, HTTPException 
from sqlmodel import select 
from models import *
from typing_extensions import TypedDict

from users import routes as user_routes 
from profiles import routes as profile_routes 
from reviews import routes as review_routes
from trips import routes as trip_routes

app = FastAPI()

@app.get('/', tags=["depchai"])
def hello():
    return "Hello World"

# User Endpoints
app.include_router(user_routes.router)

# Profile Endpoints
app.include_router(profile_routes.router)

# Review Endpoints
app.include_router(review_routes.router)

# Trip Endpoints
app.include_router(trip_routes.router)

#on start
@app.on_event("startup")
def on_startup():
    init_db()