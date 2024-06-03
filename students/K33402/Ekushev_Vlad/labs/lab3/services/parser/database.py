import datetime
from sqlmodel import Field, SQLModel, create_engine, Session
from dotenv import load_dotenv
from .config import settings

load_dotenv()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)


def create_database_session() -> Session:
    return Session(bind=engine)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


class Article(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str = Field(...)
    article_title: str = Field(...)
    processing_method: str = Field(...)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


def add_article_to_database(processing_method: str, url: str, title: str):
    db_session = create_database_session()
    new_article = Article(
        processing_method=processing_method, url=url, article_title=title
    )

    db_session.add(new_article)
    db_session.commit()
    db_session.refresh(new_article)


init_db()
