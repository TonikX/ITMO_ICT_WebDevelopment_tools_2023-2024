from sqlmodel import Session, SQLModel, create_engine


engine = create_engine('postgresql://postgres:postgres@localhost:5432/vinil_db', echo=True)
s = Session(bind=engine)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session