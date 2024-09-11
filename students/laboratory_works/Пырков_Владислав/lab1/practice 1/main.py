from fastapi import FastAPI
from db import project_db
from typing import Optional, List
from typing_extensions import TypedDict
from shemas import *

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/teams_list")
def teams_list():
    return project_db

@app.get("/team/{team_id}")
def teams_list(team_id: int):
    return [team for team in project_db if team.get("id") == team_id]

@app.post("/team")
def teams_list(team: dict):
    project_db.append(team)
    return {"status": 200, "data": team}

@app.delete("/team/delete{team_id}")
def team_delete(team_id: int):
    for i, team in enumerate(project_db):
        if team.get("id") == team_id:
            project_db.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/team{team_id}")
def team_update(team_id: int, team: dict):
    for i, war in enumerate(project_db):
        if war.get("id") == team_id:
            project_db[i] = team
    return project_db

