from sqlmodel import create_engine, Session

eng = r'A:\Studies\Веб\laboratory_work_1\database.db'
sqlite_url = f'sqlite:///{eng}'
engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)