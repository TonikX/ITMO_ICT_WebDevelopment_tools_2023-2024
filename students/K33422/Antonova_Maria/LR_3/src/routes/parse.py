from fastapi import APIRouter
from fastapi import Depends

from src.settings.connection import get_session
from src.tasks.parser_url_content import parse_url_content

parse_router = APIRouter(prefix="", tags=["parser"])


@parse_router.post("/parse")
async def parse(url: str, session=Depends(get_session)):
    #sqlalchemy_worker = SqlalchemyWorker(session)
    parse_url_content.delay(url)  # вызов задачи для celery
    return {"message": "Parsing is started"}
