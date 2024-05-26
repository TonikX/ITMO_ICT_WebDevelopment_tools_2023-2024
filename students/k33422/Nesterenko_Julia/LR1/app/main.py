from fastapi import FastAPI
import uvicorn
 
from .connection import *

from .endpoints.user_endpoints import user_router
from .endpoints.trip_endpoints import trip_router
from .endpoints.usertrip_endpoints import usertrip_router
from .endpoints.step_endpoints import step_router
from .endpoints.stay_endpoints import stay_router
from .endpoints.transition_endpoints import transition_router
from .endpoints.parser_endpoint import parse_router


app = FastAPI()


app.include_router(trip_router)
app.include_router(user_router)
app.include_router(usertrip_router)
app.include_router(step_router)
app.include_router(stay_router)
app.include_router(transition_router)
app.include_router(parse_router)

"""
@app.on_event("startup")
def on_startup():
    init_db()
"""

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)

    # sudo lsof -t -i tcp:8000 | xargs kill -9
    # uvicorn main:app --reload

    # alembic revision --autogenerate -m "... added"
    # alembic upgrade head