from fastapi import FastAPI, HTTPException
import uvicorn
 
from .parse_basic import *


app = FastAPI()


@app.post("/parse")
def parse(key: str):
    try:
        if key not in URLS.keys():
            raise HTTPException(status_code=404, 
                                detail=f"Cannot find a url with key {key}")
        parse_and_save(key, URLS[key])
        return {"message": "Parsing completed. Data saved to the database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run('parser_app:app', host="localhost", port=8001, reload=True)

    # sudo lsof -t -i tcp:8001 | xargs kill -9
    # uvicorn main:app --reloads