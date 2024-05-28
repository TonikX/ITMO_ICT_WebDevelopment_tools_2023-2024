from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.settings.connection import init_db
from src.routes.profile import profile_route
from src.routes.team import team_route
from src.routes.project import project_route
from src.routes.auth import auth_route
from src.routes.parse import parse_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(profile_route)
app.include_router(team_route)
app.include_router(project_route)
app.include_router(auth_route)
app.include_router(parse_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
