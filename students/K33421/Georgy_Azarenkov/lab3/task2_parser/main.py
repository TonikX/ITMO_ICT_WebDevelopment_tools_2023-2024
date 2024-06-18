import os

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session

app = FastAPI()


class ParseRequest(SQLModel):
    url: str


load_dotenv()
db_url = os.getenv("DB_LINK")
engine = create_engine(db_url)


class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field()


SQLModel.metadata.create_all(engine)


@app.post("/parse/")
def parse(request: ParseRequest):
    html = httpx.get(request.url)

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(id='firstHeading').text

    session = Session(engine)

    article = Article(
        title=title
    )

    session.add(article)
    session.commit()
    session.refresh(article)

    return article


@app.get("/find_all/")
def find_all():
    session = Session(engine)
    articles = session.query(Article).all()
    return articles
