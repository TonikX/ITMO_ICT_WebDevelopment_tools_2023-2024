from fastapi import APIRouter, Depends
from db import get_session
from models import Category, CategoryEnum

categoryRouter = APIRouter(prefix="/categories", tags=["category"])  # отвечает за swagger


@categoryRouter.get("/available")
async def get_available():
    return list(CategoryEnum)


@categoryRouter.get("/", response_model=list[Category])
async def get_categories(session=Depends(get_session)):
    categories = session.query(Category).all()
    return categories


@categoryRouter.get("/{category_id}", response_model=Category)
async def get_category(category_id: int, session=Depends(get_session)):
    category = session.query(Category).filter_by(id=category_id).first()
    return category


@categoryRouter.post("/")
async def create_category(category: Category, session=Depends(get_session)):
    category = Category.validate(category)
    if category.category not in CategoryEnum:
        return "Invalid category name"
    category.id = None
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@categoryRouter.patch("/{category_id}")
async def update_category(category: Category, category_id: str, session=Depends(get_session)):
    category = Category.validate(category)
    if category.category not in CategoryEnum:
        return "Invalid category name"
    category_from_db = session.query(Category).filter_by(id=category_id).first()
    if category_from_db is None:
        return "No such category"
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(category_from_db, key, value)
    session.add(category_from_db)
    session.commit()
    session.refresh(category_from_db)
    return category_from_db


@categoryRouter.delete("/{category_name}")
async def delete_category(category_name: str, session=Depends(get_session)):
    session.query(Category).filter(Category.category == category_name).delete()
    session.commit()
    return "Deleted"
