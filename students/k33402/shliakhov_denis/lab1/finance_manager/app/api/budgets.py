from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db import get_session
from app.models.models import Budget
from app.crud import crud

router = APIRouter()

@router.post("/budgets/", response_model=Budget)
def create_budget(budget: Budget, session: Session = Depends(get_session)):
    return crud.create_budget(session, budget)

@router.get("/budgets/{budget_id}", response_model=Budget)
def read_budget(budget_id: int, session: Session = Depends(get_session)):
    db_budget = crud.get_budget(session, budget_id)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@router.get("/budgets/", response_model=List[Budget])
def read_budgets(session: Session = Depends(get_session)):
    return crud.get_budgets(session)

@router.delete("/budgets/{budget_id}", response_model=Budget)
def delete_budget(budget_id: int, session: Session = Depends(get_session)):
    budget = crud.delete_budget(session, budget_id)
    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.put("/budgets/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, budget: Budget, session: Session = Depends(get_session)):
    updated_budget = crud.update_budget(session, budget_id, budget)
    if updated_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return updated_budget