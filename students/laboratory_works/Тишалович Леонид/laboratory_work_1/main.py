from fastapi import FastAPI
import uvicorn
from database import init_db
from routers.task_router import router as tasks_router
from routers.participant_router import router as participant_router
from routers.submission_router import router as submission_router
from routers.team_member_router import router as team_member_router
from routers.team_router import router as team_router
from routers.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(participant_router, prefix="/participants")
app.include_router(team_member_router, prefix="/team_members")
app.include_router(team_router, prefix="/teams")
app.include_router(tasks_router, prefix="/tasks")
app.include_router(submission_router, prefix="/submissions")

@app.on_event("startup")
def on_startup():
    init_db()