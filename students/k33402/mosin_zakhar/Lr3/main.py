import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select

from db import engine, get_session
from endpoints.user_endpoints import user_router
from endpoints.money_endpoints import main_router
from flat_mod import Flat
from models.user_models import *
from worker import parse_flat
app = FastAPI()

app.include_router(user_router)
app.include_router(main_router, prefix="/api")


def create_db():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db()


#if __name__ == '__main__':
#    uvicorn.run(app, host='localhost', port=8001)

## добавлен
@app.get("/parse/{page_num}")
async def parse_radio(page_num: int):
        parse_flat.delay(f'https://get-balance.ru/flats/?data%5BPAGE%5D%5Bname%5D=PAGE&data%5BPAGE%5D%5Bvalue%5D={page_num}')
        return {"ok": True}


@app.get("/flats")
def places_list(session=Depends(get_session)) -> List[Flat]:
    return session.exec(select(Flat)).all()