from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select

from connection import get_session
from models import Category, CategoryIn, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[Category])
def categories_list(session=Depends(get_session)):
    return session.exec(select(Category)).all()


@router.get("/{category_id}", response_model=CategoryOut)
def category_get(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=Category)
def category_create(category: CategoryIn, session=Depends(get_session)):
    category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}", response_model=dict)
def category_delete(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}


@router.patch("/{category_id}", response_model=CategoryOut)
def category_update(category_id: int, category: CategoryIn, session=Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


