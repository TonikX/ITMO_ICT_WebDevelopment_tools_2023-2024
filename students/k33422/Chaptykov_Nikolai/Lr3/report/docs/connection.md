# Соединение с бд
```Python
from sqlmodel import SQLModel, Session, create_engine

# N.B. postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
db_url = 'postgresql://postgres:123@localhost:5432/TimeManager'

engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

```