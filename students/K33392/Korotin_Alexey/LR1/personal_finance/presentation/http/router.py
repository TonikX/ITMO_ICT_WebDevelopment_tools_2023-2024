import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException

from personal_finance.presentation.http.accounts.router import account_router, tag_router
from personal_finance.presentation.http.cashflows.router import source, category
from personal_finance.presentation.http.transactions.router import transfer
from personal_finance.presentation.http.users.router import user_router

from personal_finance.infrastructure.persistance.postgres.web_page import WebPage
from sqlmodel import Session

from personal_finance.infrastructure.persistance.postgres.database import get_session

app_router = APIRouter()

load_dotenv()

PARSER_URL = os.getenv("PARSER_URL")

app_router.include_router(user_router, prefix='/users', tags=['Users'])
app_router.include_router(account_router, prefix='/accounts', tags=['Accounts'])
app_router.include_router(source, prefix='/income-source', tags=['Income sources'])
app_router.include_router(category, prefix='/expense-category', tags=['Expense categories'])
app_router.include_router(transfer, prefix='/transactions/transfer', tags=['Transfer transactions'])
app_router.include_router(tag_router, prefix='/tags', tags=['Tags'])


@app_router.post('/parse', tags=['Parsing'])
def parse(url: str) -> None:
    r = requests.post(PARSER_URL, params={'url': url})
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.json())


@app_router.post('/internal/parse-callback', tags=['Parsing'])
def parse_callback(title: str, db: Session = Depends(get_session)) -> None:
    page = WebPage(title=title)
    db.add(page)
    db.commit()
