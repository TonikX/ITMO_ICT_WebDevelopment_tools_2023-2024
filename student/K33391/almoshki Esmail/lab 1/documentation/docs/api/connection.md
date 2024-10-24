# Database Connection

## Connection Setup
```python

from sqlmodel import Session, create_engine
import dotenv
import os

dotenv.load_dotenv()

engine_url = os.getenv("ENGINE_URL")

engine = create_engine(engine_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```