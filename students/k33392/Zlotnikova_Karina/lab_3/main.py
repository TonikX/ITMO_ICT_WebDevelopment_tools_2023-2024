
import uvicorn
from fastapi import FastAPI

from db import init_db
from endpoints.main_endpoints import main_router
from endpoints.user_endpoints import user_router
from endpoints.vinil_endpoints import vinil_router

app = FastAPI()
app.include_router(user_router)
app.include_router(main_router)
app.include_router(vinil_router)

@app.on_event("startup")
def on_startup():
    init_db()
if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8080, reload=True)
