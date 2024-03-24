import uvicorn
from fastapi import FastAPI

from src.controllers import router as api_router

app = FastAPI()

app.include_router(router=api_router, prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
