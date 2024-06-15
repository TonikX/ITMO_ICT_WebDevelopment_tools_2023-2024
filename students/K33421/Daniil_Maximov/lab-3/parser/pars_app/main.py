import os
from typing import Sequence

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Field, Session, select


app = FastAPI()

load_dotenv()
db_url = os.getenv("DB_LINK")
print("db url", db_url)
engine = create_engine(db_url)

class ParseUrl(SQLModel):
    url: str

class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field()


SQLModel.metadata.create_all(engine)


@app.post("/parse")
def parse(request: ParseUrl) -> Article:
    html = httpx.get(request.url)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.replace(' / Хабр', '')
    session = Session(engine)
    record = Article(title=title)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

@app.get("/get_all")
def get_all() -> Sequence[Article]:
    session = Session(engine)
    aritcles = session.exec(select(Article)).all()
    return aritcles
