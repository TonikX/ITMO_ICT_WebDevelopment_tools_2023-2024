import uvicorn
from fastapi import FastAPI
from worker import radio_parse
from fastapi import HTTPException


app = FastAPI()

radio_names = ('radio-ermitazh', 'radio-shanson', 'monte-karlo', 'eldoradio', 'jazz', 'radio-kavkaz-xit')


@app.get("/parse_radio/{radio_name}")
def parse_radio(radio_name: str):
    if radio_name not in radio_names:
        raise HTTPException(status_code=404, detail="Radio not found")
    else:
        radio_parse.delay(f'https://top-radio.ru/playlist/{radio_name}')
        return {"ok": True}
