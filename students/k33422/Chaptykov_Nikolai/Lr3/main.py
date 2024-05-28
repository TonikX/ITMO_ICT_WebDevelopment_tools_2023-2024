from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from models import BaseImageSource, BaseImage
from connection import *
from routes import router, add_imgsource, add_img
from second_task import validate_input, AsyncScrape
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)


origins = [
    "http://localhost",
    "http://0.0.0.0",
    "http://localhost:8000",
    "172.31.0.1",
    "http://172.31.0.1"
]

app = FastAPI()
app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def append_row(img_source, img_link, session=Depends(get_session)):
    img_source = BaseImageSource(url=img_source)
    img_source_json = await add_imgsource(img_source, session)
    if img_source_json.id:
        img = BaseImage(imagesource_id=img_source_json.id, url=img_link)
        result = await add_img(img, session)
        return f"Success, added data to db"
    return f"Somethin' went wrong"


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/scrape")
async def root(url: str, start: str, end: str, session=Depends(get_session)):
    if args := validate_input(None, url, start, end):
        c = AsyncScrape(*args)
        await c._calculate_async()
        for i in c.rows:
            print(f"append row: {i}")
            temp = await append_row(*i, session)
            print(temp)
        return {"message": "completed successfully"}
    return {"message": "invalid input"}



if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

"""
alembic revision --autogenerate -m "skill added"
alembic upgrade head
"""