from sqlmodel import select
from typing_extensions import TypedDict
from fastapi import FastAPI, Depends, HTTPException
from models import *
from connection import init_db, get_session
from api.user.router import router as user_router
from api.contest.router import router as contest_router
from api.participant.router import router as participant_router
from api.task.router import router as task_router
from api.work.router import router as work_router
from api.approval.router import router as approval_router
from api.team.router import router as team_router
from api.members.router import router as members_router
from api.grade.router import router as grade_router

app = FastAPI()

app.include_router(user_router)
app.include_router(contest_router)
app.include_router(participant_router)
app.include_router(task_router)
app.include_router(work_router)
app.include_router(approval_router)
app.include_router(team_router)
app.include_router(members_router)
app.include_router(grade_router)


@app.on_event("startup")
def on_startup():
    init_db()
