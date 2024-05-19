from fastapi import FastAPI

from rest.auth.router import router as auth_router
from rest.celery_router.router import router as celery_router
from rest.sprint.router import router as sprint_router
from rest.task.router import router as task_router
from rest.task_link.router import router as task_links_router

app = FastAPI()

app.include_router(task_router)
app.include_router(sprint_router)
app.include_router(task_links_router)
app.include_router(auth_router)
app.include_router(celery_router)
