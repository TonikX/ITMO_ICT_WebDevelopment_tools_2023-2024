from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from db import get_session
from url_parser import parse_and_save
from models import Article
import uvicorn

app = FastAPI()

@app.post("/parse")
def parse(url: str, background_tasks: BackgroundTasks, session=Depends(get_session)):
    try:
        background_tasks.add_task(parse_and_save, url, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Parsing started"}

@app.get("/articles")
def get_articles(session=Depends(get_session)) -> list[Article]:
    articles = session.query(Article).all()
    return articles

@app.get("/article/{article_id}")
def get_article(article_id: int, session=Depends(get_session)):
    article = session.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8080, reload=True)