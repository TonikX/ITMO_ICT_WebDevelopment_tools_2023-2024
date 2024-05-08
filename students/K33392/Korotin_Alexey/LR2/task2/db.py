from sqlmodel import SQLModel, Session, create_engine, Field
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)


class WebPage(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)


def save_web_page(web_page: WebPage) -> WebPage:
    session: Session = get_session()
    session.add(web_page)
    session.commit()
    session.refresh(web_page)
    session.close()
    return web_page
