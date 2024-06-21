from sqlalchemy import create_engine

from app.database import Base

DATABASE_URL = "postgresql://postgres:123@localhost:5432/timedb"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

print("Все таблицы успешно созданы")
