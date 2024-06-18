import httpx
from fastapi import FastAPI
from sqlmodel import SQLModel

app = FastAPI()


class ParseRequest(SQLModel):
    url: str


base_url = "http://task2_parser:8081"


@app.post("/request_parse/", response_model=dict)
def parse(url: str):
    response = httpx.post(base_url + "/parse/", json={
      "url": url
    })
    return response.json()


@app.get("/request_find_all/")
def find_all():
    response = httpx.get(base_url + "/find_all/")
    return response.json()
