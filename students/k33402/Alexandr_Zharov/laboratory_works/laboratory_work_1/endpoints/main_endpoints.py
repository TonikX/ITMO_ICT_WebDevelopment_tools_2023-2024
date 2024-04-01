from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlmodel import Session

from endpoints.user_endpoints import auth_handler
from models.main_models import Balance, Target, Transactions, TargetCreate, TargetUpdate, TransactionsCreate, Category, \
    TransactionsUpdate, UserBalance, TargetResponse
from db.db import session

main_router = APIRouter()


@main_router.get("/balances/{balance_id}", response_model=UserBalance)
def get_balance(balance_id: int):
    balance = session.get(Balance, balance_id)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance


@main_router.post("/balances/{balance_id}/targets/", response_model=Target)
def create_target_for_balance(balance_id: int, target: TargetCreate, user=Depends(auth_handler.auth_wrapper)):
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    if target.category not in Category:
        raise HTTPException(status_code=400, detail="Invalid category")
    db_target = Target(**target.dict(), balance_id=balance_id)
    session.add(db_target)
    session.commit()
    session.refresh(db_target)
    return db_target


@main_router.put("/balances/{balance_id}/targets/{target_id}", response_model=Target)
def update_target_for_balance(balance_id: int, target_id: int, target: TargetUpdate, user=Depends(auth_handler.auth_wrapper)):
    db_target = session.get(Target, target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    if target.category not in Category:
        raise HTTPException(status_code=400, detail="Invalid category")
    for key, value in target.dict(exclude_unset=True).items():
        setattr(db_target, key, value)
    session.add(db_target)
    session.commit()
    session.refresh(db_target)
    return db_target


@main_router.delete("/balances/{balance_id}/targets/{target_id}")
def delete_target_for_balance(balance_id: int, target_id: int, user=Depends(auth_handler.auth_wrapper)):
    db_target = session.get(Target, target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    session.delete(db_target)
    session.commit()
    return {"message": "Target deleted"}


@main_router.get("/balances/{balance_id}/targets/", response_model=List[TargetResponse])
def get_targets_for_balance(balance_id: int):
    targets = session.query(Target).filter(Target.balance_id == balance_id).all()
    if not targets:
        raise HTTPException(status_code=404, detail="Targets not found for this balance")
    return targets


@main_router.post("/balances/{balance_id}/transactions/", response_model=Transactions)
def create_transaction_for_balance(balance_id: int, transaction: TransactionsCreate, user=Depends(auth_handler.auth_wrapper)):
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    if transaction.category not in Category:
        raise HTTPException(status_code=400, detail="Invalid category")
    db_transaction = Transactions(**transaction.dict(), balance_id=balance_id)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@main_router.put("/transactions/{transaction_id}", response_model=Transactions)
def update_transaction(transaction_id: int, transaction: TransactionsUpdate, user=Depends(auth_handler.auth_wrapper)):
    db_transaction = session.get(Transactions, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if transaction.category not in Category:
        raise HTTPException(status_code=400, detail="Invalid category")
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)

    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)

    return db_transaction


@main_router.delete("/balances/{balance_id}/transactions/{transaction_id}")
def delete_transaction_for_balance(balance_id: int, transaction_id: int, user=Depends(auth_handler.auth_wrapper)):
    db_transaction = session.get(Transactions, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(db_transaction)
    session.commit()
    return {"message": "Transaction deleted"}


@main_router.get("/balances/{balance_id}/transactions/", response_model=List[Transactions])
def get_transactions_for_balance(balance_id: int):
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    return db_balance.transactions
