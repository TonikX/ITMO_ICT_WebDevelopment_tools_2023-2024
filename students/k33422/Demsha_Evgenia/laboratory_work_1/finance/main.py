from fastapi import FastAPI
from connections import init_db
import uvicorn
from endpoints.expense_endpoints import expense_router
from user_repo.user_endpoints import user_router
from endpoints.category_endpoints import expense_category_router
from endpoints.account_endpoints import account_router


app = FastAPI()

app.include_router(user_router)
app.include_router(expense_router)
app.include_router(expense_category_router)
app.include_router(account_router)


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
