from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connections import get_session
from models import ExpenseCategory
from user_repo.user_endpoints import auth_handler
from sqlalchemy.orm import joinedload

expense_category_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


# Create a new expense category
@expense_category_router.post("/expense_categories/", tags=['expense_categories'])
async def create_expense_category(category: ExpenseCategory, session: Session = Depends(get_session),
                                  user=Depends(auth_handler.get_current_user)):
    new_category = ExpenseCategory(name=category.name, type=category.type,
                                   limit_of_expenses=category.limit_of_expenses, user_id=user.id)
    session.add(new_category)
    session.commit()
    return {"message": "Expense category created successfully"}


# Get all expense categories for a specific user
@expense_category_router.get("/expense_categories/list", tags=['expense_categories'])
async def get_expense_categories(session: Session = Depends(get_session),
                                 user=Depends(auth_handler.get_current_user)):
    user_categories = session.query(ExpenseCategory).options(joinedload(ExpenseCategory.expenses)).filter(
        ExpenseCategory.user_id == user.id).all()

    categories_with_expenses = []
    for category in user_categories:
        category_data = category.dict()
        category_data["expenses"] = [expense.dict() for expense in category.expenses]
        categories_with_expenses.append(category_data)

    return {"user_id": user.id, "categories": categories_with_expenses}


# Update an existing expense category using PATCH method
@expense_category_router.patch("/expense_categories/{category_id}", tags=['expense_categories'])
async def update_expense_category(category_id: int, category: ExpenseCategory,
                                  session: Session = Depends(get_session),
                                  user=Depends(auth_handler.get_current_user)):
    existing_category = session.query(ExpenseCategory).filter_by(id=category_id, user_id=user.id).first()
    if existing_category:
        for field, value in category.dict(exclude_unset=True).items():
            setattr(existing_category, field, value)
        session.commit()
        return {"message": "Expense category updated successfully"}
    raise HTTPException(status_code=404, detail="Expense category not found")


# Delete an existing expense category using DELETE method
@expense_category_router.delete("/expense_categories/{category_id}", tags=['expense_categories'])
async def delete_expense_category(category_id: int, session: Session = Depends(get_session),
                                  user=Depends(auth_handler.get_current_user)):
    existing_category = session.query(ExpenseCategory).filter_by(id=category_id, user_id=user.id).first()
    if existing_category:
        session.delete(existing_category)
        session.commit()
        return {"message": "Expense category deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense category not found")
