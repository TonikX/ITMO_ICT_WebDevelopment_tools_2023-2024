from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from connection import get_session
from auth_services import get_current_user
from models import CategoryDefault, Category, User
from typing_extensions import TypedDict
from base_responses import MessageResponse

router = APIRouter()

class CategoryResponse(TypedDict):
    status: int
    data: Category

class CategoriesListResponse(TypedDict):
    status: int
    data: List[Category]

@router.post("/", response_model=CategoryResponse)
async def categories_create(category: CategoryDefault,
                            session: AsyncSession = Depends(get_session)) -> CategoryResponse:
    category = Category.model_validate(category)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return {"status": 200, "data": category}

# Получение списка категорий
@router.get("/", response_model=CategoriesListResponse)
async def get_categories(session: AsyncSession = Depends(get_session)) -> CategoriesListResponse:
    categories = await session.execute(select(Category))
    return {"status": 200, "data": categories.scalars().all()}

# Получение категории по ID
@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, 
                       session: AsyncSession = Depends(get_session)) -> CategoryResponse:
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"status": 200, "data": category}

# Обновление категории
@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, 
                          category_data: CategoryDefault, 
                          session: AsyncSession = Depends(get_session)) -> CategoryResponse:
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category_data.dict().items():
        setattr(category, key, value)
    await session.commit()
    await session.refresh(category)
    return {"status": 200, "data": category}

# Удаление категории
@router.delete("/{category_id}")
async def delete_category(category_id: int, 
                          session: AsyncSession = Depends(get_session)) -> MessageResponse:
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()
    return {"status": 200, "message": "Category deleted"}