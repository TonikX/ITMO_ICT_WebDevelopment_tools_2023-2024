from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, List, Union
from typing_extensions import TypedDict
from sqlmodel import select

from models import *
from connection import *

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.on_event("startup")
def on_startup():
    init_db()

# sudo lsof -t -i tcp:8000 | xargs kill -9
# uvicorn main:app --reload

# TRIP
# all trips
@app.get("/trip/all", response_model=List[TripDetailed])
def trip_list(session=Depends(get_session)) -> List[Trip]:
    return session.exec(select(Trip)).all()

# one trip
@app.get("/trip/{trip_id}", response_model=TripDetailed)
def trip_one(trip_id: int, session=Depends(get_session)) -> Trip:
    #return session.exec(select(Trip).where(Trip.id == trip_id)).first()
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

# add trip
@app.post("/trip")
def trip_create(trip: TripDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": Trip}):
    trip = Trip.model_validate(trip)
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return {"status": 200, "data": trip}

# delete trip
@app.delete("/trip/delete/{trip_id}")
def trip_delete(trip_id: int, session=Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()
    return {"status": 201, "message": f"deleted trip with id {trip_id}"}

# update trip
@app.patch("/trip/{trip_id}", response_model=TripDetailed)
def trip_update(trip_id: int, trip: TripDefault, session=Depends(get_session)) -> Trip:
    db_trip = session.get(Trip, trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip_data = trip.model_dump(exclude_unset=True)
    for key, value in trip_data.items():
        setattr(db_trip, key, value)
    session.add(db_trip)
    session.commit()
    session.refresh(db_trip)
    return db_trip


# USER
# all users
@app.get("/user/all")
def user_list(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

# one user
@app.get("/user/{user_id}")
def user_one(user_id: int, session=Depends(get_session)) -> User:
    #return session.exec(select(User).where(User.id == user_id)).first()
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# add user
@app.post("/user")
def user_create(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": User}):
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}

# delete user
@app.delete("/user/delete/{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": 201, "message": f"deleted user with id {user_id}"}

# update user
@app.patch("/user/{user_id}")
def user_update(user_id: int, user: UserDefault, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# USER-TRIP-LINK
# all links
@app.get("/usertrip/all")
def link_list(session=Depends(get_session)) -> List[UserTripLink]:
    return session.exec(select(UserTripLink)).all()

# one link
@app.get("/usertrip/{user_id}in{trip_id}")
def link_one(user_id: int, trip_id: int, session=Depends(get_session)) -> UserTripLink:
    #return session.exec(select(Trip).where(Trip.id == trip_id)).first()
    link = session.exec(select(UserTripLink).where(UserTripLink.user_id == user_id and UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="this user is not in this trip")
    return link

# add link
@app.post("/usertrip")
def link_create(link: UserTripLink, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                          "data":  UserTripLink}):
    link = UserTripLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": link}

# delete link
@app.delete("/UserTripLink/delete/{user_id}in{trip_id}")
def link_delete(user_id: int, trip_id: int, session=Depends(get_session)):
    link = session.exec(select(UserTripLink).where(UserTripLink.user_id == user_id and UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="this user is not in this trip")
    session.delete(link)
    session.commit()
    return {"status": 201, "message": f"deleted user {user_id} from trip {trip_id}"}


# STEP
# all steps
@app.get("/step/all", response_model=List[StepDetailed])
def step_list(session=Depends(get_session)) -> List[Step]:
    return session.exec(select(Step)).all()

# one step
@app.get("/step/{step_id}", response_model=StepDetailed)
def step_one(step_id: int, session=Depends(get_session)) -> Step:
    #return session.exec(select(Step).where(Step.id == step_id)).first()
    step = session.get(Step, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step

# add step
@app.post("/step")
def step_create(step: StepDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                  "data": Step}):
    step_data = step.model_dump(exclude_unset=True)
    if ((step_data.get("stay_id") == 0 and step_data.get("transition_id") == 0) 
    or (step_data.get("stay_id") != 0 and step_data.get("transition_id") != 0)):
        raise HTTPException(status_code=400, detail="Invalid data")
    if step_data.get("stay_id") == 0:
        step.stay_id = None
    if step_data.get("transition_id") == 0:
        step.transition_id = None
    step = Step.model_validate(step)
    session.add(step)
    session.commit()
    session.refresh(step)
    return {"status": 200, "data": step}

# delete step
@app.delete("/step/delete/{step_id}")
def step_delete(step_id: int, session=Depends(get_session)):
    step = session.get(Step, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    session.delete(step)
    session.commit()
    return {"status": 201, "message": f"deleted step with id {step_id}"}

# update step
@app.patch("/step/{step_id}")
def step_update(step_id: int, step: Step, session=Depends(get_session)) -> Step:
    db_step = session.get(Step, step_id)
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")
    step_data = step.model_dump(exclude_unset=True)
    for key, value in step_data.items():
        setattr(db_step, key, value)
    session.add(db_step)
    session.commit()
    session.refresh(db_step)
    return db_step


# STAY
# all stays
@app.get("/stay/all")
def stay_list(session=Depends(get_session)) -> List[Stay]:
    return session.exec(select(Stay)).all()

# one stay
@app.get("/stay/{stay_id}")
def stay_one(stay_id: int, session=Depends(get_session)) -> Stay:
    #return session.exec(select(Stay).where(Stay.id == stay_id)).first()
    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    return stay

# add stay
@app.post("/stay")
def stay_create(stay: StayDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": Stay}):
    stay = Stay.model_validate(stay)
    session.add(stay)
    session.commit()
    session.refresh(stay)
    return {"status": 200, "data": stay}

# delete stay
@app.delete("/stay/delete/{stay_id}")
def stay_delete(stay_id: int, session=Depends(get_session)):
    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    session.delete(stay)
    session.commit()
    return {"status": 201, "message": f"deleted stay with id {stay_id}"}

# update stay
@app.patch("/stay/{stay_id}")
def stay_update(stay_id: int, stay: StayDefault, session=Depends(get_session)) -> Stay:
    db_stay = session.get(Stay, stay_id)
    if not db_stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    stay_data = stay.model_dump(exclude_unset=True)
    for key, value in stay_data.items():
        setattr(db_stay, key, value)
    session.add(db_stay)
    session.commit()
    session.refresh(db_stay)
    return db_stay


# TRANSITION
# all transitions
@app.get("/transition/all")
def transition_list(session=Depends(get_session)) -> List[Transition]:
    return session.exec(select(Transition)).all()

# one transition
@app.get("/transition/{transition_id}")
def transition_one(transition_id: int, session=Depends(get_session)) -> Transition:
    #return session.exec(select(Transition).where(Transition.id == transition_id)).first()
    transition = session.get(Transition, transition_id)
    if not transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    return transition

# add transition
@app.post("/transition")
def transition_list(transition: TransitionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                           "data": Transition}):
    transition = Transition.model_validate(transition)
    session.add(transition)
    session.commit()
    session.refresh(transition)
    return {"status": 200, "data": transition}

# delete transition
@app.delete("/transition/delete/{transition_id}")
def transition_delete(transition_id: int, session=Depends(get_session)):
    transition = session.get(Transition, transition_id)
    if not transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    session.delete(transition)
    session.commit()
    return {"status": 201, "message": f"deleted transition with id {transition_id}"}

# update transition
@app.patch("/transition/{transition_id}")
def transition_update(transition_id: int, transition: TransitionDefault, session=Depends(get_session)) -> Transition:
    db_transition = session.get(Transition, transition_id)
    if not db_transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    transition_data = transition.model_dump(exclude_unset=True)
    for key, value in transition_data.items():
        setattr(db_transition, key, value)
    session.add(db_transition)
    session.commit()
    session.refresh(db_transition)
    return db_transition