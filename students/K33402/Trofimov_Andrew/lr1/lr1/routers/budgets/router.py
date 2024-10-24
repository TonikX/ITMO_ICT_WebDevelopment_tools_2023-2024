from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from conn import get_session
from dependencies import verify_jwt
from models import Budget

from .models import DeletedBudgetResponse

router = APIRouter(prefix="/budgets", dependencies=[Depends(verify_jwt)])


@router.post("/", response_model=Budget)
def create_budget(budget: Budget, session: Session = Depends(get_session)) -> Budget:
    budget = Budget.model_validate(budget)
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


@router.get("/{budget_id}", response_model=Budget)
def get_budget(budget_id: int, session: Session = Depends(get_session)) -> Optional[Budget]:
    return session.get(Budget, budget_id)


@router.put("/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, budget: Budget, session: Session = Depends(get_session)) -> Budget:
    budget_obj = session.get(Budget, budget_id)
    if not budget_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Budget not found")
    budget_obj.sqlmodel_update(budget.model_dump(exclude_unset=True))
    session.add(budget_obj)
    session.commit()
    session.refresh(budget_obj)
    return budget_obj


@router.delete("/{budget_id}", response_model=DeletedBudgetResponse)
def delete_budget(budget_id: int, session: Session = Depends(get_session)) -> DeletedBudgetResponse:
    budget_obj = session.get(Budget, budget_id)
    if not budget_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Budget not found")
    session.delete(budget_obj)
    session.commit()
    return {"message": "Budget deleted successfully"}
