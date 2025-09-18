from sqlmodel import SQLModel, Session, create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DB_ADMIN')

engine = create_engine(db_url, echo=True)


def init_db():
  with Session(engine) as session:
    # Вручную удаляем таблицы в правильном порядке
    session.execute(text('DROP TABLE IF EXISTS exchangerequest CASCADE'))
    session.execute(text('DROP TABLE IF EXISTS book CASCADE'))
    session.execute(text('DROP TABLE IF EXISTS profile CASCADE'))
    session.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
    session.commit()
    
  SQLModel.metadata.drop_all(engine)
  SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session