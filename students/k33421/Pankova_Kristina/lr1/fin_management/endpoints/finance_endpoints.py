from fastapi import APIRouter, HTTPException, Security, security, Depends

from authentification.auth import AuthHandler

from sqlalchemy.exc import NoResultFound
from models.models import *
from models.user_models import *
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select

from db.connection import *
from typing_extensions import TypedDict
fin_router = APIRouter()

app = FastAPI()
app.include_router(fin_router)

fin_router = APIRouter()
auth_handler = AuthHandler()

@app.get("/categories")
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories

@app.get("/category/{category_id}")
def get_category(category_id: int, session: Session = Depends(get_session)):
    try:
        category = session.get(Category, category_id)
        return category
    except NoResultFound:
        return {"message": "Category not found"}

@app.post("/category")
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# BudgetTransaction API endpoints
@app.get("/budget_transactions")
def get_budget_transactions(session: Session = Depends(get_session)):
    budget_transactions = session.exec(select(BudgetTransaction)).all()
    return budget_transactions

@app.get("/budget_transaction/{budget_transaction_id}")
def get_budget_transaction(budget_transaction_id: int, session: Session = Depends(get_session)):
    try:
        budget_transaction = session.get(BudgetTransaction, budget_transaction_id)
        return budget_transaction
    except NoResultFound:
        return {"message": "Budget Transaction not found"}

@app.post("/budget_transaction")
def create_budget_transaction(budget_transaction: BudgetTransaction, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user)):
    budget_transaction.user = user
    budget_transaction.user_id = user.id
    session.add(budget_transaction)
    session.commit()
    session.refresh(budget_transaction)
    return budget_transaction

# FinancialTransaction API endpoints
@app.get("/financial_transactions")
def get_financial_transactions(session: Session = Depends(get_session)):
    financial_transactions = session.exec(select(FinancialTransaction)).all()
    return financial_transactions

@app.get("/financial_transaction/{financial_transaction_id}")
def get_financial_transaction(financial_transaction_id: int, session: Session = Depends(get_session)):
    try:
        financial_transaction = session.get(FinancialTransaction, financial_transaction_id)
        return financial_transaction
    except NoResultFound:
        return {"message": "Financial Transaction not found"}

@app.post("/financial_transaction")
def create_financial_transaction(financial_transaction: FinancialTransaction, session: Session = Depends(get_session), user=Depends(auth_handler.get_current_user)):
    financial_transaction.user = user
    financial_transaction.user_id = user.id
    session.add(financial_transaction)
    session.commit()
    session.refresh(financial_transaction)
    return financial_transaction

# Goal API endpoints
@app.get("/goals")
def get_goals(session: Session = Depends(get_session)):
    goals = session.exec(select(Goal)).all()
    return goals

@app.get("/goal/{goal_id}")
def get_goal(goal_id: int, session: Session = Depends(get_session)):
    try:
        goal = session.get(Goal, goal_id)
        return goal
    except NoResultFound:
        return {"message": "Goal not found"}

@app.post("/goal")
def create_goal(goal: Goal, session: Session = Depends(get_session)):
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal
