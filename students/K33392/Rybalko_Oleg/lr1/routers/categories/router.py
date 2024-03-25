from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from conn import get_session
from dependencies import verify_jwt
from models import Category

from .models import CategoryRead, DeletedCategoryResponse

router = APIRouter(prefix="/categories", dependencies=[Depends(verify_jwt)])


@router.post("/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)) -> Category:
    category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, session: Session = Depends(get_session)) -> Category:
    if (category := session.get(Category, category_id)) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: Category, session: Session = Depends(get_session)) -> Category:
    category_obj = session.get(Category, category_id)
    if not category_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Category not found")
    category_obj.sqlmodel_update(category.model_dump(exclude_unset=True))
    session.add(category_obj)
    session.commit()
    session.refresh(category_obj)
    return category_obj


@router.delete("/{category_id}", response_model=DeletedCategoryResponse)
def delete_category(category_id: int, session: Session = Depends(get_session)) -> DeletedCategoryResponse:
    category_obj = session.get(Category, category_id)
    if not category_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Category not found")
    session.delete(category_obj)
    session.commit()
    return {"message": "Category deleted successfully"}
