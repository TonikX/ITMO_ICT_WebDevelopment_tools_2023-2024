from fastapi import FastAPI

from ..rest.sprint.router import router as sprint_router
from ..rest.task.router import router as task_router
from ..rest.task_link.router import router as task_links_router

app = FastAPI()

app.include_router(task_router)
app.include_router(sprint_router)
app.include_router(task_links_router)
