from fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import TravelShow, TravelBase, Travel, TravelTogether, TravelTogetherBase, TravelTogetherShow
from connection import get_session
from typing_extensions import TypedDict

travel_router = APIRouter()

@travel_router.post("/create")
def travel_create(travel: TravelBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Travel}):
    travel = Travel.model_validate(travel)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}


@travel_router.get("/list")
def travels_list(session=Depends(get_session)) -> list[Travel]:
    return session.query(Travel).all()


@travel_router.get("/{travel_id}",  response_model=TravelShow)
def travel_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(Travel, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subtravel not found")
    return obj


@travel_router.patch("/update/{travel_id}")
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


@travel_router.delete("/delete/{travel_id}")
def travel_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}


@travel_router.post("/together-create")
def traveltogether_create(travel: TravelTogetherBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": TravelTogether}):
    travel = TravelTogether.model_validate(travel)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}


@travel_router.get("/list-traveltogethers")
def traveltogethers_list(session=Depends(get_session)) -> list[TravelTogether]:
    return session.query(TravelTogether).all()


@travel_router.get("/traveltogether/{travel_id}",  response_model=TravelTogetherShow)
def traveltogether_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(TravelTogether, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="travel not found")
    return obj


@travel_router.patch("/traveltogether/update/{travel_id}")
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


@travel_router.delete("/traveltogether/delete/{travel_id}")
def traveltogether_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(TravelTogether, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}