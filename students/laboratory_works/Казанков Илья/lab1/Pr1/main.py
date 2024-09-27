from fastapi import FastAPI, HTTPException
from models import Place, Area
from typing import Optional, List, Dict
from database import temp_bd

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/areas_list", response_model=List[Area])
def areas_list() -> List[Area]:
    return temp_bd


@app.get("/area/{area_id}", response_model=Area)
def areas_get(area_id: int) -> Area:
    for area in temp_bd:
        if area.id == area_id:
            return area
    raise HTTPException(status_code=404, detail="Area not found")


@app.post("/area", response_model=Dict[str, Area])
def areas_create(area: Area) -> Dict[str, Area]:
    new_id = max([a.id for a in temp_bd]) + 1 if temp_bd else 1
    area.id = new_id
    temp_bd.append(area)
    return {"status": 200, "data": area}


@app.delete("/area/delete/{area_id}", response_model=Dict[str, str])
def area_delete(area_id: int):
    for i, area in enumerate(temp_bd):
        if area.id == area_id:
            temp_bd.pop(i)
            return {"status": "201", "message": "deleted"}
    raise HTTPException(status_code=404, detail="Area not found")


@app.put("/area/{area_id}", response_model=Area)
def area_update(area_id: int, updated_area: Area) -> Area:
    for i, area in enumerate(temp_bd):
        if area.id == area_id:
            updated_area.id = area_id  # Убедитесь, что ID не меняется
            temp_bd[i] = updated_area
            return updated_area
    raise HTTPException(status_code=404, detail="Area not found")
