from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models import Balance, Category, Transaction, TransactionsCreate, TransactionsUpdate, UserRead, BalanceRead, CategoryRead, TransactionRead, User

from db import session
from user_endpoints import auth_handler

main_router = APIRouter()

@main_router.get("/users/{user_id}", response_model=UserRead)
def get_user_with_balance_and_categories(user_id: int):
    user = (session.query(User)
            .options(joinedload(User.balance)
                     .joinedload(Balance.categories)
                     .joinedload(Category.transactions))
            .filter(User.id == user_id)
            .first())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@main_router.get("/balances/{user_id}", response_model=BalanceRead)
def get_balance_with_categories(user_id: int):
    balance = (session.query(Balance)
               .options(joinedload(Balance.categories)
                        .joinedload(Category.transactions))
               .filter(Balance.user_id == user_id)
               .first())
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@main_router.get("/categories/{category_id}", response_model=CategoryRead)
def get_category_with_transactions(category_id: int):
    category = (session.query(Category)
                .options(joinedload(Category.transactions))
                .filter(Category.id == category_id)
                .first())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@main_router.post("/transactions/", response_model=TransactionRead)
def create_transaction(transaction: TransactionsCreate, user=Depends(auth_handler.auth_wrapper)):
    db_transaction = Transaction(**transaction.dict())
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@main_router.put("/transactions/{transaction_id}", response_model=TransactionRead)
def update_transaction(transaction_id: int, transaction_data: TransactionsUpdate, user=Depends(auth_handler.auth_wrapper)):
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction.category_id = transaction_data.category_id
    transaction.type = transaction_data.type
    transaction.value = transaction_data.value
    session.commit()
    return transaction

@main_router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, user=Depends(auth_handler.auth_wrapper)):
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"message": "Transaction deleted"}

@main_router.post("/balances/{balance_id}/categories/", response_model=CategoryRead)
def create_category(balance_id: int, category: Category, user=Depends(auth_handler.auth_wrapper)):
    db_balance = session.get(Balance, balance_id)
    if not db_balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    new_category = Category(**category.dict(), balance_id=balance_id)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

@main_router.put("/categories/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category_data: Category, user=Depends(auth_handler.auth_wrapper)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_data.name
    category.limit = category_data.limit
    session.commit()
    return category

@main_router.delete("/categories/{category_id}")
def delete_category(category_id: int, user=Depends(auth_handler.auth_wrapper)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"message": "Category deleted"}