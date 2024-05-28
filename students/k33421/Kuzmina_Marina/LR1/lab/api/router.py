from fastapi import APIRouter

# Создаем объект APIRouter
router = APIRouter()

# Определяем маршруты
@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.put("/items/{item_id}")
async def update_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

