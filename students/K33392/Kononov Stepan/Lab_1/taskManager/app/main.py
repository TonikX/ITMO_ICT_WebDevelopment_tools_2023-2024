from fastapi import FastAPI
from app.routers import auth, user, task, project, priority, category

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router, tags=["users"])
app.include_router(task.router, tags=["tasks"])
app.include_router(project.router, tags=["projects"])
app.include_router(priority.router, tags = ["priorities"])
app.include_router(category.router, tags=["categories"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=3000)
