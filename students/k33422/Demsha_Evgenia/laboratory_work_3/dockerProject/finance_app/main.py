from fastapi import FastAPI, HTTPException, Depends
from connections import init_db, get_session
from sqlalchemy.orm import Session
import requests
import uvicorn
from endpoints.expense_endpoints import expense_router
from user_repo.user_endpoints import user_router
from endpoints.category_endpoints import expense_category_router
from endpoints.account_endpoints import account_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/parse_crypto/num", tags=['parser'])
def crypto_parser(num: int, session: Session = Depends(get_session)):
    try:
        response = requests.post(
            url=f"http://parser_app:8001/parse_cryptocurrencies/num?num={num}"
        )
        response.raise_for_status()
        return {"message": "Parsing successful"}
    except:
        raise HTTPException(status_code=500, detail="Parsing unsuccessful")


@app.post("/celery_parse_books/num", tags=['parser'])
def celery_crypto_parser(num: int, session: Session = Depends(get_session)):
    headers = {"accept": "application/json"}
    try:
        response = requests.post(
            f"http://parser_app:8001/celery_parse_cryptocurrencies/num?num={num}",
            headers=headers,
        )
        response.raise_for_status()
        return {"message": "Parsing successful"}
    except:
        raise HTTPException(status_code=500, detail="Parsing unsuccessful")

app.include_router(user_router)
app.include_router(expense_router)
app.include_router(expense_category_router)
app.include_router(account_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
