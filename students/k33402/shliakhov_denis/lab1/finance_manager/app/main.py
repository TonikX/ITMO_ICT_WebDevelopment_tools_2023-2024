from fastapi import FastAPI

from app.api import routes
from app.api import users
from app.api import transactions
from app.api import categories
from app.api import budgets

app = FastAPI()

app.include_router(routes.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(budgets.router)
@app.get("/")
def read_root():
    return {"message": "Finance Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)