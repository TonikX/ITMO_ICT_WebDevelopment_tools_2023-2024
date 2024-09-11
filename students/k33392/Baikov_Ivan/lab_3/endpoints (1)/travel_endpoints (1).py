from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlmodel import Session, select

from db import db_session as session, get_session
from endpoints.user_endpoints import auth_handler

from models.travel_models import *

travel_router = APIRouter()

@travel_router.get("/places/{place_id}")
def get_place(place_id: int):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place did not found")
    return place

@travel_router.post("/places")
def create_place(def_place: Place_Default):
    place = Place.model_validate(def_place)
    session.add(place)
    session.commit()
    session.refresh(place)
    return {"status": 200, "data": place}

@travel_router.get("/places_list")
def places_list(session=Depends(get_session)) -> List[Place]:
    return session.exec(select(Place)).all()

@travel_router.delete("/places/delete/{place_id}")
def place_delete(place_id: int, session=Depends(get_session)):
    place = session.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place did not found")
    session.delete(place)
    session.commit()
    return {"ok": True}

@travel_router.patch("/places/{place_id}")
def place_update(place_id: int, place: Place_Default, session=Depends(get_session)) -> Place_Default:
    db_place = session.get(Place, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Place did not found")
    place_data = place.model_dump(exclude_unset=True)
    for key, value in place_data.items():
        setattr(db_place, key, value)
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    return db_place

@travel_router.get("/routes/{route_id}")
def get_route(route_id: int):
    route = session.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route did not found")
    return route

@travel_router.post("/routes")
def create_route(def_route: Route_Default):
    route = Route.model_validate(def_route)
    session.add(route)
    session.commit()
    session.refresh(route)
    return {"status": 200, "data": route}

@travel_router.get("/routes_list")
def routes_list(session=Depends(get_session)) -> List[Route]:
    return session.exec(select(Route)).all()

@travel_router.delete("/routes/delete/{route_id}")
def route_delete(route_id: int, session=Depends(get_session)):
    route = session.get(Route, route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route did not found")
    session.delete(route)
    session.commit()
    return {"ok": True}

@travel_router.patch("/routes/{route_id}")
def route_update(route_id: int, route: Route_Default, session=Depends(get_session)) -> Route_Default:
    db_route = session.get(Route, route_id)
    if not db_route:
        raise HTTPException(status_code=404, detail="Route did not found")
    route_data = route.model_dump(exclude_unset=True)
    for key, value in route_data.items():
        setattr(db_route, key, value)
    session.add(db_route)
    session.commit()
    session.refresh(db_route)
    return db_route


@travel_router.get("/orders/{route_id}/{place_id}")
def get_order(route_id: int, place_id: int):
    order = session.query(Order).filter(Order.route_id == route_id, Order.place_id == place_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order did not found")
    return order

@travel_router.post("/orders")
def create_order(def_order: Order):
    order = Order.model_validate(def_order)
    route = session.get(Route, order.route_id)
    place = session.get(Place, order.place_id)
    if (not route) or (not place):
        raise HTTPException(status_code=404, detail="Impossible id")
    session.add(order)
    session.commit()
    session.refresh(order)
    return {"status": 200, "data": order}

@travel_router.get("/orders_list")
def orders_list(session=Depends(get_session)) -> List[Order]:
    return session.exec(select(Order)).all()

@travel_router.delete("/orders/delete/{route_id}/{place_id}")
def order_delete(route_id: int, place_id: int, session=Depends(get_session)):
    order = session.get(Order, (route_id,place_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order did not found")
    session.delete(order)
    session.commit()
    return {"ok": True}

@travel_router.patch("/orders/{route_id}/{place_id}")
def order_update(route_id: int, place_id: int, order: Order_Default, session=Depends(get_session)) -> Order:
    db_order = session.get(Order, (route_id,place_id))
    if not db_order:
        raise HTTPException(status_code=404, detail="Order did not found")
    order_data = order.model_dump(exclude_unset=True)
    for key, value in order_data.items():
        setattr(db_order, key, value)
    route = session.get(Route, route_id)
    place = session.get(Place, place_id)
    if (not route) or (not place):
        raise HTTPException(status_code=404, detail="Impossible id")
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@travel_router.get("/journeys/{journey_id}")
def get_journey(journey_id: int):
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey did not found")
    return journey

@travel_router.post("/journeys")
def create_journey(def_journey: Journey_Default, user=Depends(auth_handler.get_current_user)):
    journey = Journey(name=def_journey.name, descryption=def_journey.descryption, user_id=user.id)
    session.add(journey)
    session.commit()
    session.refresh(journey)
    return {"status": 200, "data": journey}

@travel_router.get("/journeys_list")
def journey_list(session=Depends(get_session)) -> List[Journey]:
    return session.exec(select(Journey)).all()

@travel_router.delete("/journeys/delete/{journey_id}")
def journey_delete(journey_id: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey did not found")
    if journey.user_id != user.id:
        raise HTTPException(status_code=404, detail="You can't delete this journey")
    session.delete(journey)
    session.commit()
    return {"ok": True}

@travel_router.patch("/journeys/{journey_id}")
def journey_update(journey_id: int, journey: Journey_Redact, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> Journey_Redact:
    db_journey = session.get(Journey, journey_id)
    if not db_journey:
        raise HTTPException(status_code=404, detail="Journey did not found")
    if db_journey.user_id != user.id:
        raise HTTPException(status_code=404, detail="You can't delete this journey")
    journey_data = journey.model_dump(exclude_unset=True)
    for key, value in journey_data.items():
        setattr(db_journey, key, value)
    route = session.get(Route, db_journey.route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Impossible id")
    session.add(db_journey)
    session.commit()
    session.refresh(db_journey)
    return db_journey



@travel_router.get("/travels/{journey_id}")
def get_travel(journey_id: int, user=Depends(auth_handler.get_current_user)):
    travel = session.query(Travel).filter(Travel.journey_id == journey_id, Travel.user_id == user.id).first()
    if not travel:
        raise HTTPException(status_code=404, detail="Travel did not found")
    return travel

@travel_router.post("/travels/{journey_id}")
def create_travel(journey_id: int, def_travel: Travel_Default, user=Depends(auth_handler.get_current_user)):

    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Impossible id")
    travel = Travel(journey_id = journey_id, descryption=def_travel.descryption, user_id=user.id)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}

@travel_router.get("/travels_list")
def travels_list(session=Depends(get_session)) -> List[Travel]:
    return session.exec(select(Travel)).all()

@travel_router.delete("/travels/delete/{journey_id}")
def travel_delete(journey_id: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    travel = session.get(Travel, (user.id, journey_id))
    if not travel:
        raise HTTPException(status_code=404, detail="Travel did not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}

@travel_router.patch("/travels/{journey_id}")
def travel_update(journey_id: int, travel: Travel_Default, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> Travel:
    db_travel = session.get(Travel, (user.id, journey_id))
    if not db_travel:
        raise HTTPException(status_code=404, detail="Travel did not found")
    travel_data = travel.model_dump(exclude_unset=True)
    for key, value in travel_data.items():
        setattr(db_travel, key, value)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel

@travel_router.get("/find_people/{journey_id}")
def find_people(journey_id: int, session=Depends(get_session)):
    users_ids = session.exec(select(Travel.user_id).where(Travel.journey_id == journey_id))
    if not users_ids:
        raise HTTPException(status_code=404, detail="Journey did not found")
    names = []
    for user_id in users_ids:
        username = session.get(User, user_id)
        if username:
            names.append(username.username)
    return names