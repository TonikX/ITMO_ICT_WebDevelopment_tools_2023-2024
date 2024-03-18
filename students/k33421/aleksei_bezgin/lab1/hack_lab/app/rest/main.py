from fastapi import APIRouter

from app.rest.auth.router import router as auth_router
from app.rest.teams.router import router as teams_router
from app.rest.tasks.router import router as tasks_router
from app.rest.hackathons.router import router as hackathons_router
from app.rest.submissions.router import router as submissions_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(teams_router, prefix="/teams", tags=["teams"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(hackathons_router, prefix="/hackathons", tags=["hackathons"])
api_router.include_router(submissions_router, prefix="/submissions", tags=["submissions"])