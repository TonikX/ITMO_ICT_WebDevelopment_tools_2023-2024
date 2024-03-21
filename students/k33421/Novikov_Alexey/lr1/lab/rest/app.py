from fastapi import FastAPI

from lab.rest.auth.router import router
from lab.rest.sprint.router import router as sprint_router
from lab.rest.task.router import router as task_router
from lab.rest.task_link.router import router as task_links_router

app = FastAPI()

app.include_router(task_router)
app.include_router(sprint_router)
app.include_router(task_links_router)
app.include_router(router)
