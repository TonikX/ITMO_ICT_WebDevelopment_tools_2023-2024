from fastapi import FastAPI
from typing import Optional, List, Union
from typing_extensions import TypedDict

from .models import * 

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


temp_bd = [
    {
        "id": 1,
        "status": "open",
        "member_capacity": 5,
        "members": 
            [{
                "id": 1,
                "first_name": "Bob",
                "last_name": "Ross",
                "gender": "m",
                "age": 55,
                "telephone": "+79234536171",
                "email": "ross@mail.com",
                "bio": "Professional painter and traveller"
            },
            {
                "id": 2,
                "first_name": "Kate",
                "last_name": "Moss",
                "gender": "f",
                "age": 40,
                "telephone": "+79142330981",
                "email": "k_moss@mail.com",
                "bio": "Role and runway model"
            }],
        "steps": 
            [{
                "id": 1,
                "date_from": "2024-03-20 12:00",
                "date_to": "2024-03-20 13:00",
                "est_price": 399,
                "contents": {
                    "id": 1,
                    "location_from": "Paris, France",
                    "location_to": "London, UK",
                    "transport": "plane"
                    },
            },
            {
                "id": 2,
                "date_from": "2024-03-20 14:00",
                "date_to": "2024-03-24 12:00",
                "est_price": 600,
                "contents": {
                    "id": 1,
                    "location": "London, UK",
                    "address": "Baker Street 221B",
                    "accomodation": "hotel",
                    },
            }],
    },  
    {
        "id": 2,
        "status": "cancelled",
        "member_capacity": None,
        "members": 
            [{
                "id": 1,
                "first_name": "Bob",
                "last_name": "Ross",
                "gender": "m",
                "age": 55,
                "telephone": "+79234536171",
                "email": "ross@mail.com",
                "bio": "Professional painter and traveller"
            }],
        "steps": 
            [{
                "id": 3,
                "date_from": "2024-03-01 23:00",
                "date_to": "2024-03-02 15:00",
                "est_price": 100,
                "contents": {
                    "id": 2,
                    "location_from": "Larnaka, Cyprus",
                    "location_to": "Mykonos, Greece",
                    "transport": "ship"
                    },
            }],
    },  
]


user_bd = []
step_bd = []
transition_bd = []
stay_bd = []

"""
NO ANNOTATIONS

# all trips
@app.get("/trip/all")
def trip_list():
    return temp_bd

# one trip
@app.get("/trip/{trip_id}")
def trip_list(trip_id: int):
    return [trip for trip in temp_bd if trip.get("id") == trip_id]

# add trip
@app.post("/trip")
def trip_list(trip: dict):
    temp_bd.append(trip)
    return {"status": 200, "data": trip}

# delete trip
@app.delete("/trip/delete/{trip_id}")
def trip_delete(trip_id: int):
    for i, trip in enumerate(temp_bd):
        if trip.get("id") == trip_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted trip with id {trip_id}"}

# update trip
@app.put("/trip/{trip_id}")
def trip_update(trip_id: int, trip: dict):
    for tr in temp_bd:
        if tr.get("id") == trip_id:
            tr = trip
    return temp_bd

"""

# TRIP
# all trips
@app.get("/trip/all")
def trip_list() -> List[Trip]:
    return temp_bd

# one trip
@app.get("/trip/{trip_id}")
def trip_list(trip_id: int) -> List[Trip]:
    return [trip for trip in temp_bd if trip.get("id") == trip_id]

# add trip
@app.post("/trip")
def trip_list(trip: Trip) -> TypedDict('Response', {"status": int, "data": Trip}):
    trip_to_append = trip.model_dump()
    temp_bd.append(trip_to_append)
    return {"status": 200, "data": trip}

# delete trip
@app.delete("/trip/delete/{trip_id}")
def trip_delete(trip_id: int):
    for i, trip in enumerate(temp_bd):
        if trip.get("id") == trip_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted trip with id {trip_id}"}

# update trip
@app.put("/trip/{trip_id}")
def trip_update(trip_id: int, trip: Trip) -> List[Trip]:
    for tr in temp_bd:
        if tr.get("id") == trip_id:
            trip_to_append = trip.model_dump()
            temp_bd.remove(trip)
            temp_bd.append(trip_to_append)
    return temp_bd


# USER
# all users
@app.get("/user/all")
def user_list() -> List[User]:
    unique_users = []
    unique_ids = []
    for trip in temp_bd:
        new_users = [user for user in trip.get("members") if user.get("id") not in unique_ids]
        unique_users.extend(new_users)
        unique_ids.extend([user.get("id") for user in new_users])
    return unique_users
    # OR return user_bd

# one user
@app.get("/user/{user_id}")
def user_list(user_id: int) -> List[User]:
    relevant_users = []
    for trip in temp_bd:
        relevant_users = [user for user in trip.get("members") if user.get("id") == user_id]
        if len(relevant_users) > 0:
            break
    return relevant_users
    # OR return [user for user in user_bd if user.get("id") == user_id]

# add user
@app.post("/user")
def user_list(user: User) -> TypedDict('Response', {"status": int, "data": User}):
    user_to_append = user.model_dump()
    user_bd.append(user_to_append)
    return {"status": 200, "data": user}

# delete user
@app.delete("/user/delete/{user_id}")
def user_delete(user_id: int):
    for i, user in enumerate(user_bd):
        if user.get("id") == user_id:
            user_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted user with id {user_id}"}

# update user
@app.put("/user/{user_id}")
def user_update(user_id: int, user: User) -> List[User]:
    for us in user_bd:
        if us.get("id") == user_id:
            user_to_append = user.model_dump()
            user_bd.remove(user)
            user_bd.append(user_to_append)
    return user_bd


# STEP
# all steps
@app.get("/step/all")
def step_list() -> List[Step]:
    unique_steps = []
    unique_ids = []
    for trip in temp_bd:
        new_steps = [step for step in trip.get("steps") if step.get("id") not in unique_ids]
        unique_steps.extend(new_steps)
        unique_ids.extend([step.get("id") for step in new_steps])
    return unique_steps
    # OR return step_bd


# one step
@app.get("/step/{step_id}")
def step_list(step_id: int) -> List[Step]:
    relevant_steps = []
    for trip in temp_bd:
        relevant_steps = [step for step in trip.get("steps") if step.get("id") == step_id]
        if len(relevant_steps) > 0:
            break
    return relevant_steps
    # OR return [step for step in step_bd if step.get("id") == step_id]

# add step
@app.post("/step")
def step_list(step: Step) -> TypedDict('Response', {"status": int, "data": Step}):
    step_to_append = step.model_dump()
    step_bd.append(step_to_append)
    return {"status": 200, "data": step}

# delete step
@app.delete("/step/delete/{step_id}")
def step_delete(step_id: int):
    for i, step in enumerate(step_bd):
        if step.get("id") == step_id:
            step_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted step with id {step_id}"}

# update step
@app.put("/step/{step_id}")
def step_update(step_id: int, step: Step) -> List[Step]:
    for st in step_bd:
        if st.get("id") == step_id:
            step_to_append = step.model_dump()
            step_bd.remove(step)
            step_bd.append(step_to_append)
    return step_bd


# STAY
# all stays
@app.get("/stay/all")
def stay_list() -> List[Stay]:
    return stay_bd

# one stay
@app.get("/stay/{stay_id}")
def stay_list(stay_id: int) -> List[Stay]:
    return [stay for stay in stay_bd if stay.get("id") == stay_id]

# add stay
@app.post("/stay")
def stay_list(stay: Stay) -> TypedDict('Response', {"status": int, "data": Stay}):
    stay_to_append = stay.model_dump()
    stay_bd.append(stay_to_append)
    return {"status": 200, "data": stay}

# delete stay
@app.delete("/stay/delete/{stay_id}")
def stay_delete(stay_id: int):
    for i, stay in enumerate(stay_bd):
        if stay.get("id") == stay_id:
            stay_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted stay with id {stay_id}"}

# update stay
@app.put("/stay/{stay_id}")
def stay_update(stay_id: int, stay: Stay) -> List[Stay]:
    for st in stay_bd:
        if st.get("id") == stay_id:
            stay_to_append = stay.model_dump()
            stay_bd.remove(stay)
            stay_bd.append(stay_to_append)
    return stay_bd


# TRANSITION
# all transitions
@app.get("/transition/all")
def transition_list() -> List[Transition]:
    return transition_bd

# one transition
@app.get("/transition/{transition_id}")
def transition_list(transition_id: int) -> List[Transition]:
    return [transition for transition in transition_bd if transition.get("id") == transition_id]

# add transition
@app.post("/transition")
def transition_list(transition: Transition) -> TypedDict('Response', {"status": int, "data": Transition}):
    transition_to_append = transition.model_dump()
    transition_bd.append(transition_to_append)
    return {"status": 200, "data": transition}

# delete transition
@app.delete("/transition/delete/{transition_id}")
def transition_delete(transition_id: int):
    for i, transition in enumerate(transition_bd):
        if transition.get("id") == transition_id:
            transition_bd.pop(i)
            break
    return {"status": 201, "message": f"deleted transition with id {transition_id}"}

# update transition
@app.put("/transition/{transition_id}")
def transition_update(transition_id: int, transition: Transition) -> List[Transition]:
    for tr in transition_bd:
        if tr.get("id") == transition_id:
            transition_to_append = transition.model_dump()
            transition_bd.remove(transition)
            transition_bd.append(transition_to_append)
    return transition_bd
