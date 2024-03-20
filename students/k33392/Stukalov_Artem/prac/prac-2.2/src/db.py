from sqlmodel import SQLModel, Session, create_engine

db_url = "postgresql://tutor03:tutor03@127.0.0.1/web_prac_2"
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
