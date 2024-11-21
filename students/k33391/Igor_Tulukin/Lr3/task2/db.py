from sqlmodel import SQLModel, Session, create_engine
import psycopg2
from psycopg2 import sql
from fastapi import HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DB_ADMIN")

db_url = f"{db_url}"
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


def save_to_db(url: str, title: str):
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO page (url, title) VALUES (%s, %s)", (url, title))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()