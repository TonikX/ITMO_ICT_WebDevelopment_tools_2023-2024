from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
Base = declarative_base()
load_dotenv()
db_url = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session

def init_db():
    Base.metadata.create_all(bind=engine)
