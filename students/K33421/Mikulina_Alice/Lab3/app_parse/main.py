from fastapi import FastAPI, HTTPException
import requests
import asyncio
import uvicorn
from pydantic import BaseModel
from parsers.parser import parse_and_save

# urls = [
#     'https://mybooklist.ru/list/1029',
#     'https://mybooklist.ru/list/483',
#     'https://mybooklist.ru/list/1204',
#     'https://mybooklist.ru/list/480'
# ]


class ParseModel(BaseModel):
    url: str
    user_id: int


app = FastAPI()

@app.get("/")
def hello():
    return "Hello, [username]!"

@app.post("/parse")
async def parse(request: ParseModel):
    try:
        result = await parse_and_save(request.url, request.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)