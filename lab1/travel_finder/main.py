from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db.connection import init_db
from endpoints.interest_endpoints import interest_router, user_interest_router
from endpoints.trip_endpoints import trip_router
from endpoints.user_endpoints import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(user_interest_router)
app.include_router(interest_router, prefix="/interests", tags=["interests"])
app.include_router(trip_router, prefix="/trips", tags=["trips"])

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
