import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from connection import init_db
from endpoints.location_endpoints import location_router
from endpoints.transport_endpoints import transport_router
from endpoints.trip_endpoints import trip_router
from endpoints.user_endpoints import user_router
from endpoints.user_trip_link_endpoints import user_trip_link_router

app = FastAPI()

app.include_router(trip_router)
app.include_router(user_router)
app.include_router(user_trip_link_router)
app.include_router(location_router)
app.include_router(transport_router)


app.add_event_handler("startup", init_db)

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
