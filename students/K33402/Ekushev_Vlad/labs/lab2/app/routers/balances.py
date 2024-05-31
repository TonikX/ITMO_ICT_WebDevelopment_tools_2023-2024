from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core import db
from app.models.main import (
    Balance,
    Target,
    Transactions,
    TargetCreate,
    TargetUpdate,
    TransactionsCreate,
    Category,
    TargetResponse,
    CategoryTransactionLink,
    CategoryTargetLink,
    UserBalance,
)
from app.models.user import User
import app.services.auth as auth_service
from starlette import status

router = APIRouter()


@router.get("/{balance_id}", tags=["balances"], response_model=UserBalance)
def get_balance(
    balance_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
) -> UserBalance:
    balance = session.get(Balance, balance_id)
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found"
        )
    return UserBalance(
        id=balance.id,
        user_id=balance.user_id,
        balance=balance.balance,
        transactions=balance.transactions,
        targets=balance.targets,
    )


@router.post("/{balance_id}/targets/", response_model=Target, tags=["targets"])
def create_target_for_balance(
    balance_id: int,
    target: TargetCreate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
) -> Target:
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found"
        )

    category = session.exec(
        select(Category).where(Category.id == target.category_id)
    ).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category"
        )

    db_target = Target(value=target.value, balance_id=balance_id)
    session.add(db_target)
    session.commit()

    category_target_link = CategoryTargetLink(
        category_id=target.category_id, target_id=db_target.id
    )
    session.add(category_target_link)
    session.commit()

    session.refresh(db_target)

    return db_target


@router.put(
    "/{balance_id}/targets/{target_id}",
    tags=["targets"],
    response_model=Target,
)
def update_target_for_balance(
    balance_id: int,
    target_id: int,
    target: TargetUpdate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
) -> Target:
    db_target = session.get(Target, target_id)
    if db_target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Target not found"
        )

    category = session.exec(
        select(Category).where(Category.id == target.category_id)
    ).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category"
        )

    for key, value in target.dict(exclude_unset=True).items():
        setattr(db_target, key, value)
    session.add(db_target)
    session.commit()
    session.refresh(db_target)

    db_category_target_link = session.exec(
        select(CategoryTargetLink).where(CategoryTargetLink.target_id == target_id)
    ).one()
    session.delete(db_category_target_link)
    category_target_link = CategoryTargetLink(
        category_id=target.category_id, target_id=target_id
    )
    session.add(category_target_link)
    session.commit()

    return db_target


@router.delete("/{balance_id}/targets/{target_id}", tags=["targets"])
def delete_target_for_balance(
    balance_id: int,
    target_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_target = session.get(Target, target_id)
    if db_target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Target not found"
        )
    session.delete(db_target)
    session.commit()
    return {"message": "Target deleted"}


@router.get(
    "/{balance_id}/targets/",
    tags=["targets"],
    response_model=List[TargetResponse],
)
def get_targets_for_balance(
    balance_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    targets = session.exec(select(Target).where(Target.balance_id == balance_id)).all()
    if not targets:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Targets not found for this balance",
        )
    return targets


@router.post(
    "/{balance_id}/transactions/",
    tags=["transactions"],
    response_model=Transactions,
)
def create_transaction_for_balance(
    balance_id: int,
    transaction: TransactionsCreate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
) -> Transactions:
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")

    category = session.exec(
        select(Category).where(Category.id == transaction.category_id)
    ).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Invalid category")

    db_transaction = Transactions(
        value=transaction.value, type=transaction.type, balance_id=balance_id
    )
    session.add(db_transaction)

    if transaction.type == "income":
        db_balance.balance += transaction.value
    elif transaction.type == "expenses":
        db_balance.balance -= transaction.value

    session.add(db_balance)
    session.commit()

    category_transaction_link = CategoryTransactionLink(
        category_id=transaction.category_id, transaction_id=db_transaction.id
    )
    session.add(category_transaction_link)
    session.commit()

    session.refresh(db_transaction)

    return db_transaction


@router.delete("/{balance_id}/transactions/{transaction_id}", tags=["transactions"])
def delete_transaction_for_balance(
    balance_id: int,
    transaction_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_transaction = session.get(Transactions, transaction_id)
    if db_transaction is None or db_transaction.balance is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if db_transaction.type == "income":
        db_transaction.balance.balance -= db_transaction.value
    elif db_transaction.type == "expenses":
        db_transaction.balance.balance += db_transaction.value

    session.delete(db_transaction)
    session.commit()
    return {"message": "Transaction deleted"}


@router.get(
    "/{balance_id}/transactions/",
    tags=["transactions"],
    response_model=List[Transactions],
)
def get_transactions_for_balance(
    balance_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_balance = session.get(Balance, balance_id)
    if db_balance is None:
        raise HTTPException(status_code=404, detail="Balance not found")
    return db_balance.transactions
