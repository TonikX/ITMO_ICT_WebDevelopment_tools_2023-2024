from fastapi import FastAPI
import uvicorn
from connection import init_db, get_session
from endpoints.location_endpoint import location_router
from endpoints.auth_endpoint import auth_router
from endpoints.user_endpoint import user_router
from endpoints.travel_endpoint import travel_router


app = FastAPI()

app.include_router(location_router, prefix="/locations", tags=["locations"])
app.include_router(travel_router, prefix="/travels", tags=["travels"])
app.include_router(auth_router, prefix="/", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])

@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)


