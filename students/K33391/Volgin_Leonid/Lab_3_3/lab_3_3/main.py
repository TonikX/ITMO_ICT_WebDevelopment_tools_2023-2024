from fastapi import FastAPI, HTTPException
#from models.main_models import *
from db import init_db
from user_endpoints import user_router
from main_endpoints import main_router

from worker import radio_parse
app = FastAPI()

app.include_router(user_router)
app.include_router(main_router, prefix="/api")


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

@app.get('/')
def hello():
    return 'hello'



@app.on_event("startup")
def on_startup():
    init_db()




radio_names = ('radio-ermitazh', 'radio-shanson', 'monte-karlo', 'eldoradio', 'jazz', 'radio-kavkaz-xit')


@app.get("/parse_radio/{radio_name}")
async def parse_radio(radio_name: str):
    if radio_name not in radio_names:
        raise HTTPException(status_code=404, detail="Radio not found")
    else:
        radio_parse.delay(f'https://top-radio.ru/playlist/{radio_name}')
        return {"ok": True}

#if __name__ == '__main__':
#    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
    #create_db_and_tables()