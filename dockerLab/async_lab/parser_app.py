from fastapi import FastAPI, HTTPException
import requests
from async_lab.task2_asyncio import parse_all_urls, data_handlers


app = FastAPI()


@app.post("/parse/:category")
async def parse(url: str):
    try:
        category = url.split("/")[-1]
        response = requests.get(url)
        response.raise_for_status()
        total_added = await parse_all_urls(data_handlers.get(category), url, 5)

        return {"message": "Parsing completed", "total_added": total_added}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
