from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from ..core import db
from ..models.main import (
    CategoriesTargetResponse,
    Category,
    CategoryCreate,
    CategoryResponse,
    CategoryTargetLink,
    CategoryTransactionLink,
    CategoryUpdate,
    Target,
    TransactionResponse,
    Transactions,
)
from ..models.user import User
from ..services import auth as auth_service


router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    categories = session.exec(select(Category)).all()
    category_responses = []

    for category in categories:
        transactions = session.exec(
            select(Transactions)
            .join(
                CategoryTransactionLink,
            )
            .where(CategoryTransactionLink.transaction_id == Transactions.id)
            .where(CategoryTransactionLink.category_id == category.id)
        ).all()

        targets = session.exec(
            select(Target)
            .join(CategoryTargetLink)
            .where(CategoryTargetLink.target_id == Target.id)
            .where(CategoryTargetLink.category_id == category.id)
        ).all()

        transaction_responses = [
            TransactionResponse(
                id=transaction.id, value=transaction.value, type=transaction.type
            )
            for transaction in transactions
        ]
        target_responses = [
            CategoriesTargetResponse(id=target.id, value=target.value)
            for target in targets
        ]
        category_response = CategoryResponse(
            id=category.id,
            type=category.type,
            transactions=transaction_responses,
            targets=target_responses,
        )
        category_responses.append(category_response)

    return category_responses


@router.post("/", response_model=Category)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_category = Category(type=category.type)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_category = session.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete(
    "/{category_id}",
)
def delete_category(
    category_id: int,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_category = session.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(db_category)
    session.commit()
    return {"message": "Category deleted"}
