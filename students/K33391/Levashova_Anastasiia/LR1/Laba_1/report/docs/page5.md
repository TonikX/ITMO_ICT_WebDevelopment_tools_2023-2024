# Полтзователи
## Эндпоинты для пользователей

Были реализованы следующие эндпоинты:

* получение списка пользователей;
* получение пользователя по id;
* создание пользователя;
* удаление пользователя;
* изменение пользователя;
* получение списка задач для зарегистрированного пользователя;


Код реализации:

    from typing import List
    from fastapi import HTTPException, Depends, APIRouter
    from sqlmodel import select
    from typing_extensions import TypedDict
    from models import User, UserDefault, Task, TasksDetails
    from connection import get_session
    from api.auth import get_current_user
    
    
    router = APIRouter()
    
    
    @router.get("/")
    def users_list(session=Depends(get_session)) -> List[User]:
        return session.exec(select(User)).all()
    
    
    @router.get("/{user_id}")
    def get_label(user_id: int, session=Depends(get_session)) -> User:
        return session.get(User, user_id)
    
    
    @router.post("/")
    def user_create(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                "data": User}):
        user = User.model_validate(user)
        user.set_password(user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 200, "data": user}
    
    
    @router.delete("/{user_id}")
    def delete_user(user_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"is_deleted": True}
    
    
    @router.patch("/{user_id}")
    def update_user(user_id: int, user: UserDefault, session=Depends(get_session)) -> UserDefault:
        db_users = session.get(User, user_id)
        if not db_users:
            raise HTTPException(status_code=404, detail="Label not found")
        categories_data = user.model_dump(exclude_unset=True)
        for key, value in categories_data.items():
            setattr(db_users, key, value)
        session.add(db_users)
        session.commit()
        session.refresh(db_users)
        return db_users
    
    @router.get("/tasks", response_model=List[Task])
    async def get_user_tasks(
        current_user: User = Depends(get_current_user),
        session = Depends(get_session)
    ) -> List[Task]:
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
        tasks_query = select(Task).where(Task.user_id == current_user.id)
        tasks = session.exec(tasks_query).all()
        return tasks
