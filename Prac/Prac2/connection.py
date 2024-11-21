from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:password@localhost:5432/timetable'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
