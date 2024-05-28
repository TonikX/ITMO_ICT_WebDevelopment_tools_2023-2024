from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from conn import get_session
from dependencies import verify_jwt
from models import Budget, BudgetCategoryLink, Category

router = APIRouter(prefix="/categories/{category_id}/budgets", dependencies=[Depends(verify_jwt)])


@router.post("/{budget_id}")
def add_budget_to_category(category_id: int, budget_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Category not found")

    budget = session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Budget not found")

    link = BudgetCategoryLink(budget_id=budget_id, category_id=category_id)
    session.add(link)
    session.commit()
    return {"message": "Budget added to category successfully"}


@router.delete("/{budget_id}")
def remove_budget_from_category(category_id: int, budget_id: int, session: Session = Depends(get_session)):
    link = session.query(BudgetCategoryLink).filter_by(category_id=category_id, budget_id=budget_id).first()
    if not link:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Budget is not linked to the category")

    session.delete(link)
    session.commit()
    return {"message": "Budget removed from category successfully"}
