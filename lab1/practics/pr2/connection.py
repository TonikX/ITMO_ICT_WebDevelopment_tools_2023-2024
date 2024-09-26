from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:1216@localhost/warriors_db'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session