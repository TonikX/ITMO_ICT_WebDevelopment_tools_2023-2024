from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.routes.parse2 import parse_router



app = FastAPI()
app.include_router(parse_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
