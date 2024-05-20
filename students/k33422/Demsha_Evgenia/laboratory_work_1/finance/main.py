from fastapi import FastAPI, Depends

import repos.expense_repo
from models import User, Account, ExpenseCategory, SourceOfIncome, Income, Expense
from connections import init_db, get_session
from typing import TypedDict, List
from sqlmodel import select
import uvicorn


app = FastAPI()


@app.get("/")
def hello():
    return "Hello world!"


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/user")
def user_create(user: User, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": User}):
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


@app.post("/category")
def category_create(category: ExpenseCategory, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": ExpenseCategory}):
    category = ExpenseCategory.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"status": 200, "data": category}


@app.get("/categories_list")
def categories_list(session=Depends(get_session)) -> List[ExpenseCategory]:
    return session.exec(select(ExpenseCategory)).all()


@app.get("/category/{category_id}")
def categories_get(category_id: int, session=Depends(get_session)) -> ExpenseCategory:
    return session.exec(select(ExpenseCategory).where(ExpenseCategory.id == category_id)).first()


@app.get("/expenses")
def expenses_list():
    expenses = repos.expense_repo.select_all_expenses()
    return {"expenses": expenses}


@app.get("/expense/{id}")
def expenses_get():
    expenses = repos.expense_repo.select_expense(id)
    return {"expense": expense}


@app.post("/expense")
def create_expense(expense: Expense):
    expense = Expense(amount=expense.amount, user_id=expense.user_id, category_id=expense.category_id, account_id=expense.account_id)



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
