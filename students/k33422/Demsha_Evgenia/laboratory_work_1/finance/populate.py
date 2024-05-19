import random
from sqlmodel import Session, select
from connections import engine
from models import User, Account, ExpenseCategory, SourceOfIncome, Income, Expense


def create_category(cat_name):
    cat = ExpenseCategory(name=cat_name, user_id=1, type="expense")
    return cat


def create_expense(cat_id, am):
    expense = Expense(amount=am, user_id=1, category_id=cat_id, account_id=1)
    return expense


def add_to_db():

    with Session(engine) as session:
        account = Account(name="debit card", balance=10000, user_id=1)
        session.add(account)
        session.commit()

        cat_names = ["food", "transport", "beauty"]
        cats = [create_category(x) for x in cat_names]
        session.add_all(cats)
        session.commit()

        expenses = [create_expense(random.randrange(1,4), x * random.randrange(10, 50, 10)) for x in range(10)]
        session.add_all(expenses)
        session.commit()


if __name__ == "__main__":
    add_to_db()
