from fastapi import APIRouter, HTTPException, Depends
from typing import List

from auth import AuthHandler
from models.finance import Balance, Subscription, SubscriptionCreate, Target, Transactions, TargetCreate, TargetUpdate, TransactionsCreate, Category, TransactionsUpdate
from repositories.finance import find_balance, find_subscription, select_all_targets, find_target, find_transaction, select_all_transactions
from database import session

main_router = APIRouter()
auth_handler = AuthHandler()

@main_router.get("/balances/{balance_id}", response_model=Balance)
def get_balance(balance_id: int):
    balance = find_balance(balance_id)
    print(balance)
    if not balance:
        raise HTTPException(status_code=404, detail="Balance not found")
    return balance

@main_router.post("/balances/{balance_id}/targets/", response_model=Target)
def create_target_for_balance(balance_id: int, target: TargetCreate, user=Depends(auth_handler.auth_wrapper)):
    db_balance = find_balance(balance_id)
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
    db_target = find_target(balance_id, target_id)
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
    db_target = find_target(balance_id, target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    session.delete(db_target)
    session.commit()
    return {"message": "Target deleted"}


@main_router.get("/balances/{balance_id}/targets/", response_model=List[Target])
def get_targets_for_balance(balance_id: int):
    targets = select_all_targets(balance_id)
    if not targets:
        raise HTTPException(status_code=404, detail="Targets not found for this balance")
    return targets

#_______________________________________

@main_router.post("/balances/{balance_id}/transactions/", response_model=Transactions)
def create_transaction_for_balance(balance_id: int, transaction: TransactionsCreate, user=Depends(auth_handler.auth_wrapper)):
    db_balance = find_balance(balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    if transaction.category not in Category:
        raise HTTPException(status_code=400, detail="Invalid category")
    db_transaction = Transactions(**transaction.dict(), balance_id=balance_id)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@main_router.put("/balances/{balance_id}/transactions/{transaction_id}", response_model=Transactions)
def update_transaction(balance_id: int, transaction_id: int, transaction: TransactionsUpdate, user=Depends(auth_handler.auth_wrapper)):
    db_transaction = find_transaction(balance_id, transaction_id)
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
    db_transaction = find_transaction(balance_id, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(db_transaction)
    session.commit()
    return {"message": "Transaction deleted"}


@main_router.get("/balances/{balance_id}/transactions/", response_model=List[Transactions])
def get_transactions_for_balance(balance_id: int):
    db_transactions = select_all_transactions(balance_id)
    if db_transactions is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    
    return db_transactions

#_________________________________________________________________________________________________________-

@main_router.post("/balances/{balance_id}/subscriptions/", response_model=Subscription)
def create_subscription_for_balance(balance_id: int, subscription: SubscriptionCreate, user=Depends(auth_handler.auth_wrapper)):
    db_balance = find_balance(balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    db_subscription = Subscription(**subscription.dict(), balance_id=balance_id)
    session.add(db_subscription)
    session.commit()
    session.refresh(db_subscription)
    return db_subscription

@main_router.get("/balances/{balance_id}/subscriptions/{subscription_id}", response_model=Subscription)
def get_subscription(balance_id: int, subscription_id: int):
    db_subscription = find_subscription(balance_id, subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
    

@main_router.delete("/balances/{balance_id}/subscriptions/{subscription_id}")
def delete_subscription_for_balance(balance_id: int, subscription_id: int, user=Depends(auth_handler.auth_wrapper)):
    db_subscription = find_subscription(balance_id, subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    session.delete(db_subscription)
    session.commit()
    return {"message": "Subscription deleted"}