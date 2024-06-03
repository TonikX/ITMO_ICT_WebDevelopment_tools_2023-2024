from fastapi import FastAPI, HTTPException, Depends
import httpx
from bs4 import BeautifulSoup
from models import Article, TitleResponse, UrlRequest
from db import get_db
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()


@app.post("/parse/", response_model=TitleResponse)
async def parse_url(url_request: UrlRequest, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url_request.url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=str(e))

    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else None
    
    if not title:
        raise HTTPException(status_code=400, detail="Title not found on the page")

    article = Article(url=url_request.url, title=title)
    db.add(article)
    try:
        db.commit()
        db.refresh(article)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return TitleResponse(id=article.id, url=article.url, title=article.title)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
