from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:postgres@localhost/lab_db'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session