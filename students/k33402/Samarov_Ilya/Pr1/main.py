from fastapi import FastAPI
from models import Place, Area
from typing_extensions import TypedDict
from database import temp_bd
from typing import Optional, List

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/areas_list")
def areas_list() -> list[Area]:
    return temp_bd


@app.get("/area/{area_id}")
def areas_get(area_id: int) -> List[Area]:
    return [area for area in temp_bd if area.get("id") == area_id]


@app.post("/area")
def areas_create(area: Area) -> TypedDict('Response', {"status": int, "data": Area}):
    area_to_append = area.model_dump()
    temp_bd.append(area_to_append)
    return {"status": 200, "data": area}


@app.delete("/area/delete{area_id}")
def area_delete(area_id: int):
    for i, area in enumerate(temp_bd):
        if area.get("id") == area_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/area{area_id}")
def area_update(area_id: int, area: Area) -> List[Area]:
    for war in temp_bd:
        if war.get("id") == area_id:
            area_to_append = area.model_dump()
            temp_bd.remove(war)
            temp_bd.append(area_to_append)
    return temp_bd