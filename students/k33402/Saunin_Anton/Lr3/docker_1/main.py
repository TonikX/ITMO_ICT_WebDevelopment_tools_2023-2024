from fastapi import FastAPI
from database import init_db
from endpoints.location import location_router
from endpoints.travel import travel_router
from endpoints.auth import auth_router
from endpoints.user import user_router
from endpoints.parse import parse_router

app = FastAPI()

app.include_router(location_router, prefix="/api/locations", tags=["locations"])
app.include_router(travel_router, prefix="/api/travels", tags=["travels"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(parse_router, prefix="/api", tags=["parse"])


@app.on_event("startup")
def on_startup():
    init_db()
