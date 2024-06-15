from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:12345@localhost/lab1'
engine = create_engine(db_url)


def init_db():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
