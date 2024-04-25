from fastapi import APIRouter
from app.models.healthcheck import Healthcheck

router = APIRouter()


@router.get("/health")
async def healthcheck() -> Healthcheck:
    return Healthcheck(ok="true")
