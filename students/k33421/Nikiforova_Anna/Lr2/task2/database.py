from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from config import LOGIN, PASSWORD, HOST, PORT, DB_NAME


DATABASE_URI = f"postgresql+psycopg://{LOGIN}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
ASYNC_DATABASE_URI = f"postgresql+psycopg_async://{LOGIN}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

async_engine = create_async_engine(ASYNC_DATABASE_URI)
AsyncSession = async_sessionmaker(bind=async_engine)
