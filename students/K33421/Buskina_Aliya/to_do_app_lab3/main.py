from fastapi import FastAPI

from routes.task_routes import router as task_router
from routes.user_routes import router as user_router
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from fastapi_users import FastAPIUsers


app = FastAPI(
    title="ToDone",
    description="API для менеджера задач",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    print("Initializing database...")
    init_db()
    print("Database initialized.")

user_tags_metadata = {"Operations related to users"}
task_tags_metadata = {"Operations related to tasks"}

app.include_router(user_router, tags=[user_tags_metadata])
app.include_router(task_router, tags=[task_tags_metadata])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


