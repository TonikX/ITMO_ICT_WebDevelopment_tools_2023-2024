from fastapi import FastAPI

import db

from routers import *
from models import *

app = FastAPI()
app.include_router(task_router)
app.include_router(tag_router)
app.include_router(priority_router)
app.include_router(project_router)
app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    db.init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=3000)
