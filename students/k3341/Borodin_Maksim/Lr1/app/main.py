from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.notifications import router as notifications_router
from app.api.priorities import router as priorities_router
from app.api.schedules import router as schedules_router
from app.api.tasks import router as tasks_router
from app.api.time_tracks import router as time_tracks_router
from app.api.users import router as users_router

app = FastAPI(title="Time Manager API")


@app.get("/")
def root() -> dict[str, str]:
    # базовый healthcheck, чтобы быстро понять что api поднято
    return {"message": "Time Manager API is running"}


# роутеры разделены по предметным зонам, так проще поддерживать код
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(priorities_router)
app.include_router(tasks_router)
app.include_router(time_tracks_router)
app.include_router(schedules_router)
app.include_router(notifications_router)
