
import uvicorn
from fastapi import FastAPI, HTTPException
from db import init_db
from endpoints.travel_endpoints import travel_router
from endpoints.user_endpoints import user_router
from worker import product_parse

app = FastAPI()
app.include_router(travel_router, prefix="/travel")
app.include_router(user_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get('/')
def hello():
    return 'hello'


prod_names = ('uglovye-kukhni',
               'kukhni',
               'elementy-kukhni',
               'obedennye-gruppy',
               'khity-prodazh-kukhni',
               'kukhonnye-ugolki',
               'mojki',
               )

@app.get("/parse/{prod_name}")
async def parse_radio(prod_name: str):
    if prod_name not in prod_names:
        raise HTTPException(status_code=404, detail="Product did not found")
    else:
        product_parse.delay(f'https://yourroom.ru/{prod_name}')
        return {"ok": True}

#if __name__ == '__main__':
#    uvicorn.run('main:app', host="localhost", port=8080, reload=True)