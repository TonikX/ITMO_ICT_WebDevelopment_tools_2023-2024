from fastapi import FastAPI
import uvicorn
from database import init_db, get_session
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import *
from database import get_session
from typing_extensions import TypedDict

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/travel-create")
def travel_create(travel: TravelBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Travel}):
    travel = Travel.model_validate(travel)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}


@app.get("/list-travels")
def travels_list(session=Depends(get_session)) -> list[Travel]:
    return session.query(Travel).all()


@app.get("/travel/{travel_id}",  response_model=TravelShow)
def travel_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(Travel, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subtravel not found")
    return obj


@app.patch("/travel/update/{travel_id}")
def travel_update(travel_id: int, travel: TravelBase, session=Depends(get_session)) -> Travel:
    db_travel = session.get(Travel, travel_id)
    if not db_travel:
        raise HTTPException(status_code=404, detail="travel not found")

    travel_data = travel.model_dump(exclude_unset=True)
    for key, value in travel_data.items():
        setattr(db_travel, key, value)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel


@app.delete("/travel/delete/{travel_id}")
def travel_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}


@app.post("/travel-together-create")
def traveltogether_create(travel: TravelTogetherBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": TravelTogether}):
    travel = TravelTogether.model_validate(travel)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}


@app.get("/list-traveltogethers")
def traveltogethers_list(session=Depends(get_session)) -> list[TravelTogether]:
    return session.query(TravelTogether).all()


@app.get("/traveltogether/{travel_id}",  response_model=TravelTogetherShow)
def traveltogether_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(TravelTogether, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="travel not found")
    return obj


@app.patch("/traveltogether/update/{travel_id}")
def traveltogether_update(travel_id: int, travel: TravelTogetherBase, session=Depends(get_session)) -> TravelTogether:
    db_travel = session.get(TravelTogether, travel_id)
    if not db_travel:
        raise HTTPException(status_code=404, detail="travel not found")

    travel_data = travel.model_dump(exclude_unset=True)
    for key, value in travel_data.items():
        setattr(db_travel, key, value)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel


@app.delete("/traveltogether/delete/{travel_id}")
def traveltogether_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(TravelTogether, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}


@app.post("/area-create")
def area_create(area: AreaBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Area}):
    area = Area.model_validate(area)
    session.add(area)
    session.commit()
    session.refresh(area)
    return {"status": 200, "data": area}


@app.get("/list-areas")
def areas_list(session=Depends(get_session)) -> list[Area]:
    return session.query(Area).all()


@app.get("/area/{area_id}",  response_model=AreaShow)
def area_get(area_id: int, session=Depends(get_session)):
    obj = session.get(Area, area_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subarea not found")
    return obj


@app.patch("/area/update/{area_id}")
def area_update(area_id: int, area: AreaBase, session=Depends(get_session)) -> Area:
    db_area = session.get(Area, area_id)
    if not db_area:
        raise HTTPException(status_code=404, detail="area not found")

    area_data = area.model_dump(exclude_unset=True)
    for key, value in area_data.items():
        setattr(db_area, key, value)
    session.add(db_area)
    session.commit()
    session.refresh(db_area)
    return db_area


@app.delete("/area/delete/{area_id}")
def area_delete(area_id: int, session=Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="area not found")
    session.delete(area)
    session.commit()
    return {"ok": True}


@app.post("/place-create")
def place_create(place: PlaceBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Place}):
    place = Place.model_validate(place)
    session.add(place)
    session.commit()
    session.refresh(place)
    return {"status": 200, "data": place}


@app.get("/list-places-in-area/{area_id}")
def places_list(area_id: int, session=Depends(get_session)) -> list[Place]:
    return session.query(Place).filter(Place.area_id == area_id).all()


@app.get("/place/{place_id}",  response_model=PlaceShow)
def place_get(place_id: int, session=Depends(get_session)):
    obj = session.get(Place, place_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subplace not found")
    return obj


@app.patch("/place/update/{place_id}")
def place_update(place_id: int, place: PlaceBase, session=Depends(get_session)) -> Place:
    db_place = session.get(place, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="place not found")

    place_data = place.model_dump(exclude_unset=True)
    for key, value in place_data.items():
        setattr(db_place, key, value)
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    return db_place


@app.delete("/place/delete/{place_id}")
def place_delete(place_id: int, session=Depends(get_session)):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="place not found")
    session.delete(place)
    session.commit()
    return {"ok": True}
