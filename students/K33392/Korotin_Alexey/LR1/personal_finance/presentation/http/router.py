from fastapi import APIRouter

from personal_finance.presentation.http.accounts.router import account_router, tag_router
from personal_finance.presentation.http.cashflows.router import source, category
from personal_finance.presentation.http.transactions.router import transfer
from personal_finance.presentation.http.users.router import user_router

app_router = APIRouter()

app_router.include_router(user_router, prefix='/users', tags=['Users'])
app_router.include_router(account_router, prefix='/accounts', tags=['Accounts'])
app_router.include_router(source, prefix='/income-source', tags=['Income sources'])
app_router.include_router(category, prefix='/expense-category', tags=['Expense categories'])
app_router.include_router(transfer, prefix='/transactions/transfer', tags=['Transfer transactions'])
app_router.include_router(tag_router, prefix='/tags', tags=['Tags'])
