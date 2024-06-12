# connection.py

```
from sqlmodel import SQLModel, Session, create_engine
from models import *
```
```
# urls have the following pattern: dialect+driver://username:password@host:port/database
db_url = 'postgresql://postgres:alison28@localhost:5433/warriors'
engine = create_engine(db_url, echo=True)
```
```
def init_db():
    SQLModel.metadata.create_all(engine)
```
```
def get_session():
    with Session(engine) as session:
        yield session
```