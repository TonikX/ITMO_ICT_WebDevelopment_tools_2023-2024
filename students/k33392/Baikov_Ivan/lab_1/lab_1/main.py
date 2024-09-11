
import uvicorn
from fastapi import FastAPI
from db import init_db
from endpoints.travel_endpoints import travel_router
from endpoints.user_endpoints import user_router


app = FastAPI()
app.include_router(travel_router, prefix="/travel")
app.include_router(user_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get('/')
def hello():
    return 'hello'

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8001, reload=True)