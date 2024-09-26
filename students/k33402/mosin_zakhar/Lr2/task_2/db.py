from sqlmodel import Session, SQLModel, create_engine


engine = create_engine('postgresql://postgres:1234@localhost:5432/flat_db', echo=True)
ses = Session(bind=engine)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session