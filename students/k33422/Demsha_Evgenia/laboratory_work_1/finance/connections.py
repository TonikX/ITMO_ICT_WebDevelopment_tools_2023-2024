from sqlmodel import SQLModel, Session, create_engine
#from models import User
from models import User, Account, ExpenseCategory, SourceOfIncome, Income, Expense


db_url = 'postgresql+psycopg2://postgres:271120@localhost:5433/finance'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
