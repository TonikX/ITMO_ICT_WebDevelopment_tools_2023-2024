from connections import engine
from models import User, Account, ExpenseCategory, SourceOfIncome, Income, Expense
from sqlmodel import Session, select, or_


def select_all_expenses():
    with Session(engine) as session:
        statement = select(Expense, ExpenseCategory).join(ExpenseCategory)
       # statement = statement.where(Gem.id > 0).where(Gem.id < 2)
        #statement = statement.where(or_(Gem.id>1, Gem.price!=2000))
        result = session.exec(statement)
        res = []
        for expense, category in result:
            res.append({'expense': expense, 'category': category})

        print(res)
        return res


def select_expense(id):
    with Session(engine) as session:
        statement = select(Expense, ExpenseCategory).join(ExpenseCategory)
        statement = statement.where(Expense.id == id)
        result = session.exec(statement)
        return result.first()


# select_all_expenses()
