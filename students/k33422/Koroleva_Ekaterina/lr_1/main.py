import uvicorn
from fastapi import FastAPI

from src.config import app_settings
from src.api import v1_router

app = FastAPI(
    title=app_settings.title,
    debug=app_settings.debug
)

app.include_router(v1_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
