from multiprocessing.pool import AsyncResult
import uvicorn
from services.app.models.articles import ArticlesParseResponse, URLData
from .celery_app import parse_article
from .config import settings
from fastapi import FastAPI

app = FastAPI()


@app.post("/get-article-title/")
async def get_article_title(data: URLData):
    result: AsyncResult = parse_article.delay(str(data.url))
    return ArticlesParseResponse(ok=True, task_id=str(result))


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = parse_article.AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "PENDING"}
    elif task_result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": task_result.result}
    else:
        return {"status": "FAILURE"}


def start() -> None:
    uvicorn.run(
        "services.parser.main:app",
        host=settings.DOMAIN,
        port=settings.PARSER_PORT,
        reload=True,
    )


if __name__ == "__main__":
    start()
