from fastapi import FastAPI
from schemas import Waste, Category
from typing_extensions import TypedDict
from database import temp_bd
from typing import Optional, List
import uvicorn
app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/category_list")
def category_list() -> list[Category]:
    return temp_bd


@app.get("/category/{category_id}")
def category_get(category_id: int) -> List[Category]:
    return [category for category in temp_bd if category.get("id") == category_id]


@app.post("/category")
def category_create(category: Category) -> TypedDict('Response', {"status": int, "data": Category}):
    category_to_append = category.model_dump()
    temp_bd.append(category_to_append)
    return {"status": 200, "data": category}


@app.delete("/category/delete{category_id}")
def category_delete(category_id: int):
    for i, category in enumerate(temp_bd):
        if category.get("id") == category_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/category{category_id}")
def category_update(category_id: int, category: Category) -> List[Category]:
    for war in temp_bd:
        if war.get("id") == category_id:
            category_to_append = category.model_dump()
            temp_bd.remove(war)
            temp_bd.append(category_to_append)
    return temp_bd
