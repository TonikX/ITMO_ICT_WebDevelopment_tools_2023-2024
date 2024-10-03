from contextlib import asynccontextmanager

from fastapi import FastAPI
from connection import init_db

from api import (
    auth_api,
    user_api,
    contest_api,
    organizer_api,
    participant_api,
    team_api,
    problem_api,
    submission_api,
    parser_api
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_api.router)
app.include_router(user_api.router)
app.include_router(contest_api.router)
app.include_router(organizer_api.router)
app.include_router(participant_api.router)
app.include_router(team_api.router)
app.include_router(problem_api.router)
app.include_router(submission_api.router)
app.include_router(parser_api.router)
