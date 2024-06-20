from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import cast, Integer
from sqlalchemy.orm import Session
from finance_app.connections import get_session
from finance_app.models import Expense, ExpenseCategory, Account
from finance_app.user_repo.user_endpoints import auth_handler

expense_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


# Create a new expense
@expense_router.post("/expenses/", tags=['expenses'])
async def create_expense(expense: Expense, session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    new_expense = Expense(user_id=user.id, amount=expense.amount, transaction_date=expense.transaction_date)

    # Check if the category_id and account_id belong to the authorized user
    category = session.query(ExpenseCategory).filter_by(id=expense.category_id, user_id=user.id).first()
    account = session.query(Account).filter_by(id=expense.account_id, user_id=user.id).first()

    if category and account:
        new_expense.category_id = expense.category_id
        new_expense.account_id = expense.account_id
        session.add(new_expense)
        session.commit()
        return {"message": "Expense created successfully"}
    else:
        raise HTTPException(status_code=403, detail="Unauthorized to add this category_id or account_id")


# Get all expenses for a specific user
@expense_router.get("/expenses/list", tags=['expenses'])
async def get_expenses(session: Session = Depends(get_session),
                       user=Depends(auth_handler.get_current_user)):
    #user_expenses = session.query(Expense).filter(Expense.user_id == user_id).all()
    user_expenses = session.query(Expense).filter(Expense.user_id == cast(user.id, Integer)).all()

    return {"user_id": user.id, "expenses": user_expenses}

# Update an existing expense using PATCH method
@expense_router.patch("/expenses/{expense_id}", tags=['expenses'])
async def update_expense(expense_id: int, expense: Expense, session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    existing_expense = session.get(Expense, expense_id)

    if existing_expense:
        # Check if the expense belongs to the authorized user
        if existing_expense.user_id == user.id:
            for field, value in expense.dict(exclude_unset=True).items():
                setattr(existing_expense, field, value)
            session.commit()
            return {"message": "Expense updated successfully"}
        else:
            raise HTTPException(status_code=403, detail="Unauthorized to update this expense")

    raise HTTPException(status_code=404, detail="Expense not found")


# Delete an existing expense using DELETE method
@expense_router.delete("/expenses/{expense_id}", tags=['expenses'])
async def delete_expense(expense_id: int, session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    existing_expense = session.get(Expense, expense_id)
    if existing_expense and existing_expense.user_id == user.id:
        session.delete(existing_expense)
        session.commit()
        return {"message": "Expense deleted successfully"}
    return {"message": "Expense not found"}
