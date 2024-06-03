from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, Session
import os

load_dotenv()
db_url = os.getenv('DB_URL')

engine = create_engine(db_url, echo=True)

def get_db():
    with Session(engine) as session:
        yield session
