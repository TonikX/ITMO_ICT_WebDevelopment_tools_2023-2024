from fastapi import FastAPI
import uvicorn
from db import init_db
from endpoints import logic_router
from auth import auth_router

app = FastAPI()

app.include_router(logic_router, prefix="/api", tags=["main"])
app.include_router(auth_router, prefix="/api/users", tags=["users"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)