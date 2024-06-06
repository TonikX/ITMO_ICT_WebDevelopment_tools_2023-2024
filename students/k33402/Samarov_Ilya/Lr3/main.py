from fastapi import FastAPI
from database import init_db
from location_endpoints import location_router
from travel_endpoints import travel_router
from auth_endpoints import auth_router
from user_endpoints import user_router
from parse_ecnpoint import parse_router

app = FastAPI()

app.include_router(location_router, prefix="/api/locations", tags=["locations"])
app.include_router(travel_router, prefix="/api/travels", tags=["travels"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(parse_router, prefix="/api/users", tags=["parse"])


@app.on_event("startup")
def on_startup():
    init_db()
