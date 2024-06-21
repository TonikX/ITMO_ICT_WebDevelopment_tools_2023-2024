from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_ADMIN")

engine = create_engine(db_url, echo=True)
session = Session(bind=engine)