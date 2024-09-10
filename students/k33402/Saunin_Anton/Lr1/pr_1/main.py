from fastapi import FastAPI, HTTPException
from typing import List
from models import Area
from database import temp_bd
app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"

@app.get("/areas/", response_model=List[Area])
def area_list():
    return temp_bd

@app.get("/areas/{area_id}", response_model=Area)
def area_get(area_id: int):
    for area in temp_bd:
        if area["id"] == area_id:
            return area
    raise HTTPException(status_code=404, detail="Area not found")

@app.post("/areas/", response_model=Area)
def area_create(area: Area):
    new_area = area.dict()
    temp_bd.append(new_area)
    return new_area

@app.delete("/areas/{area_id}")
def area_delete(area_id: int):
    global temp_bd
    temp_bd = [area for area in temp_bd if area["id"] != area_id]
    return {"status": "deleted"}

@app.put("/areas/{area_id}", response_model=Area)
def area_update(area_id: int, updated_area: Area):
    for i, area in enumerate(temp_bd):
        if area["id"] == area_id:
            temp_bd[i] = updated_area.dict()
            return updated_area
    raise HTTPException(status_code=404, detail="Area not found")
