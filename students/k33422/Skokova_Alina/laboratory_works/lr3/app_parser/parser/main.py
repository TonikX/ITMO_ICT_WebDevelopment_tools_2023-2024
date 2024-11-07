from typing import List
from fastapi import FastAPI, HTTPException
from typing_extensions import TypedDict

from .task2_threading import main

app = FastAPI()

@app.post("/parse")
def parse(urls: List[str], num: int) -> TypedDict('Response', {"status": int, "message": str}):
    main(urls, num)
    return {"status": 200, "message": "Parsing completed"}