import requests
from bs4 import BeautifulSoup
import psycopg2
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from common import pars_item, PAGES, insert_into_db, create_db


def parse_and_save(url):
    for page in PAGES:
        complete_url = f'{url}{page}'
        try:
            response = requests.get(complete_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса на страницу: {complete_url}\n{e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('li', class_='s-item')

        parsed_items = []
        for item in items:
            item_res = pars_item(item)
            parsed_items.append(item_res)

        insert_into_db(parsed_items)


app = FastAPI()

class ParseRequest(BaseModel):
    url: str

@app.post("/parse/")
async def parse(request: ParseRequest):
    try:
        create_db()
        parse_and_save(request.url)
        return {"message": f"Tasks were successfully saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))