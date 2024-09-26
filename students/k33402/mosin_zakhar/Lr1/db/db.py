from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
postgres_url = os.getenv('DB_URL')

db_url = postgres_url
engine = create_engine(db_url, echo=True)
session = Session(bind=engine)