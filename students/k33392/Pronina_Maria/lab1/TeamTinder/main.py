from fastapi import FastAPI
from routers.user import router as user_router
from routers.skill import router as skill_router
from routers.userskill import router as userskill_router
from routers.userproject import router as userproject_router
from routers.team import router as team_router
from routers.userteam import router as userteam_router
from routers.teamproject import router as teamproject_router
from routers.task import router as task_router
from routers.auth import router as auth_router

from lab1.TeamTinder.connection import init_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(skill_router)
app.include_router(userskill_router)
app.include_router(userproject_router)
app.include_router(team_router)
app.include_router(userteam_router)
app.include_router(teamproject_router)
app.include_router(task_router)
