from fastapi import FastAPI
import requests
from sqlmodel import SQLModel, Field
from typing_extensions import List

app = FastAPI()


class ParseRequest(SQLModel):
    url: str

class Article(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str = Field()

@app.post("/parse_request")
def parse(url: str) -> Article:
    parser_url = "http://parse_app:8083/parse"
    response = requests.post(parser_url, json={'url': url})
    print("response",response)
    return response.json()

@app.get("/get_all_request")
def parse() -> List[Article]:
    parser_url = "http://parse_app:8083/get_all"
    response = requests.get(parser_url)
    print("response",response)
    return response.json()

