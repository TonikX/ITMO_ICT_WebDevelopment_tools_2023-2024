from sqlmodel import Field, SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

postgres_url = os.getenv('DB_ADMIN')
db_url = postgres_url
engine = create_engine(db_url, echo=True)

def create_session() -> Session:
    return Session(bind=engine)

class Article(SQLModel, table=True):
    id: int = Field(primary_key=True)
    article: str = Field()

def commit_article(title: str):
    db_session = create_session()
    db_article = Article(article=title)

    db_session.add(db_article)
    db_session.commit() 
    db_session.refresh(db_article)
