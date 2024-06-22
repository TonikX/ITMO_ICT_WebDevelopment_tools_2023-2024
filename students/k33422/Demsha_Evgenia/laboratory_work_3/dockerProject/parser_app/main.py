from fastapi import FastAPI
import uvicorn
from parser.threading_parser import crypto_parse
from parser.settings import URLS
from parser.celery_parser import celery_parse_and_save

app = FastAPI()


@app.get("/")
def main():
    return "Main page"


@app.post("/parse_cryptocurrencies/num")
def parse(num: int):
    account_post_data = crypto_parse(num)
    return account_post_data


@app.post("/celery_parse_cryptocurrencies/num")
def parse_async(num: int):
    urls_slice = URLS[:num]
    for url in urls_slice:
        celery_parse_and_save.delay(url)
    return {"message": "Parsing started"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)
