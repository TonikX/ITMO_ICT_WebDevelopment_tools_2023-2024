from fastapi import FastAPI
from typing import Optional, List
from typing_extensions import TypedDict
from models import *
app = FastAPI()


@app.get('/')
def hello():
    return "Welcome to the finest bookcrossing app"


@app.get("/users_list")
def users_list() -> List[Person]:
    return temp_bd


@app.get("/user/{warrior_id}")
def get_user(user_id: int) -> List[Person]:
    return [user for user in temp_bd if user['id'] == user_id]


@app.post('/user')
def create_user(user: Person) -> TypedDict('Response', {"status": int, "data": Person}):
    temp_bd.append(user)
    return {"status": 200, "data": user}


@app.delete('/user/delete{id}')
def delete_user(id: int):
    users = [user for user in temp_bd if user['id'] == id]
    if users:
        user = users[0]
        temp_bd.remove(user)
    return {"status": 200, "deleted data": user}


@app.put('/user/{id}')
def update_user(id: int, new_user: dict) -> Person:
    for i, user in enumerate(temp_bd):
        if user['id'] == id:
            old = user
            temp_bd[i] = new_user

    return old


temp_bd = [
    {
        "id": 1,
        "name": "Emsa",
        "age": 23,
        "profile": {
            "id": 1,
            "nickname": "Bo Mo",
            "hobbies": "Footbal",
            "skills": "Leadership"
        },
        "Books": {
            "id": 1,
            "title": "Quran",
            "author": "God",
            "edition": 1
        }
    }
]
