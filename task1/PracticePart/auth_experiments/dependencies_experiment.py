from fastapi import FastAPI, Depends
from typing import Annotated


app = FastAPI()

def const_func():
    return 1


@app.get('/')
def root(const_value:Annotated[int, Depends(const_func)]):
    return {'const_value': const_value}


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
