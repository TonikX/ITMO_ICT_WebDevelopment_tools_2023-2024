
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Budget

router = APIRouter()

@router.get("/budgets", response_model=List[Budget], tags=["budget"])
def get_budgets(session=Depends(get_session)) -> List[Budget]:
    return session.exec(select(Budget)).all()

@router.get("/budgets/{budget_id}", response_model=Budget, tags=["budget"])
def get_budget(budget_id: int, session=Depends(get_session)) -> Budget:
    budget = session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.post("/budgets", response_model=Budget, tags=["budget"])
def create_budget(budget: Budget, session=Depends(get_session)) -> Budget:
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget

@router.patch("/budgets/{budget_id}", response_model=Budget, tags=["budget"])
def update_budget(budget_id: int, budget: Budget, session=Depends(get_session)) -> Budget:
    db_budget = session.get(Budget, budget_id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget_data = budget.dict(exclude_unset=True)
    for key, value in budget_data.items():
        setattr(db_budget, key, value)
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return db_budget

@router.delete("/budgets/{budget_id}", tags=["budget"])
def delete_budget(budget_id: int, session=Depends(get_session)):
    budget = session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    session.delete(budget)
    session.commit()
    return {"ok": True}