from fastapi import FastAPI
from fastapi import FastAPI
from db import project_db
from typing import Optional, List
from typing_extensions import TypedDict
from models import *


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/teams_list")
def teams_list():
    return temp_bd

@app.get("/team/{team_id}")
def teams_list(team_id: int):
    return [team for team in temp_bd if team.get("id") == team_id]

@app.post("/team")
def teams_list(team: dict):
    temp_bd.append(team)
    return {"status": 200, "data": team}

@app.delete("/team/delete{team_id}")
def team_delete(team_id: int):
    for i, team in enumerate(temp_bd):
        if team.get("id") == team_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/team{team_id}")
def team_update(team_id: int, team: dict):
    for i, war in enumerate(temp_id):
        if war.get("id") == team_id:
            temp_id[i] = team
    return temp_id

