from fastapi import FastAPI
import uvicorn
from database import init_db
from auth_endpoints import auth_router
from user_endpoints import user_router
from task_endpoints import task_router

app = FastAPI()

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
