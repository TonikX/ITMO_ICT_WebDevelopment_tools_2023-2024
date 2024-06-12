from fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import PlaceBase, Place, PlaceShow, AreaShow, AreaBase, Area
from connection import get_session
from typing_extensions import TypedDict

location_router = APIRouter()

@location_router.post("/area-create")
def area_create(area: AreaBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Area}):
    area = Area.model_validate(area)
    session.add(area)
    session.commit()
    session.refresh(area)
    return {"status": 200, "data": area}


@location_router.get("/list-areas")
def areasList(session=Depends(get_session)) -> list[Area]:
    return session.query(Area).all()


@location_router.get("/area/{area_id}",  response_model=AreaShow)
def areaGet(area_id: int, session=Depends(get_session)):
    obj = session.get(Area, area_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subarea not found")
    return obj


@location_router.patch("/area/update/{area_id}")
def areaUpdate(area_id: int, area: AreaBase, session=Depends(get_session)) -> Area:
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


@location_router.delete("/area/delete/{area_id}")
def areaDelete(area_id: int, session=Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="area not found")
    session.delete(area)
    session.commit()
    return {"ok": True}


@location_router.post("/place-create")
def placeCreate(place: PlaceBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Place}):
    place = Place.model_validate(place)
    session.add(place)
    session.commit()
    session.refresh(place)
    return {"status": 200, "data": place}


@location_router.get("/list-places-in-area/{area_id}")
def placesList(area_id: int, session=Depends(get_session)) -> list[Place]:
    return session.query(Place).filter(Place.area_id == area_id).all()


@location_router.get("/place/{place_id}",  response_model=PlaceShow)
def placeGet(place_id: int, session=Depends(get_session)):
    obj = session.get(Place, place_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subplace not found")
    return obj


@location_router.patch("/place/update/{place_id}")
def placeUpdate(place_id: int, place: PlaceBase, session=Depends(get_session)) -> Place:
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


@location_router.delete("/place/delete/{place_id}")
def placeDelete(place_id: int, session=Depends(get_session)):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="place not found")
    session.delete(place)
    session.commit()
    return {"ok": True}