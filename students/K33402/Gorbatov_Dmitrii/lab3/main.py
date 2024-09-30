from fastapi import FastAPI

from connection import init_db
from routes import user, task, taskinfo, tag, timelog, auth, parser

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(parser.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(tag.router)
app.include_router(taskinfo.router)
app.include_router(timelog.router)
app.include_router(auth.router)
