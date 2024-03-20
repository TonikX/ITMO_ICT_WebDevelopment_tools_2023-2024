# app/Routes.py

## categories

```
router = APIRouter()


@router.get("/categories/{category_id}/tasks", response_model=List[Task])
def read_tasks_by_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    tasks = session.query(Task).join(TaskCategory).filter(TaskCategory.category_id == category_id).all()
    return tasks

@router.get("/tasks/{task_id}/categories", response_model=List[Category])
def read_categories_by_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    categories = session.query(Category).join(TaskCategory).filter(TaskCategory.task_id == task_id).all()
    return categories

@router.get("/usersall/", response_model=List[UserWithTaskNames])
def read_users_with_tasks(session: Session = Depends(get_session)):
    statement = select(User).options(joinedload(User.tasks)).distinct()
    result = session.execute(statement)
    users = result.scalars().unique().all()
    users_with_task_names = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "tasks": [{"title": task.title} for task in user.tasks]
        }
        users_with_task_names.append(UserWithTaskNames(**user_data))

    return users_with_task_names

```
## users

```
router = APIRouter()

@router.get("/users/", response_model=List[UserResponse])
def read_users(session: Session = Depends(get_session)):
    users = session.execute(select(User)).scalars().all()
    return [UserResponse(id=user.id, username=user.username) for user in users]

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=int)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(username=user.username)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user.id

@router.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username is not None:
        user.username = user_update.username
    session.commit()
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}

```

## tasks
```
router = APIRouter()


@router.post("/tasks/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.execute(select(Task)).scalars().all()
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    timelogs = session.query(TimeLog).filter(TimeLog.task_id == task_id).all()
    for timelog in timelogs:
        session.delete(timelog)

    for task_category in task.task_categories: 
        session.delete(task_category)

    session.delete(task)
    session.commit()
    return {"ok": True}

```

## tasksCategories

```
router = APIRouter()



@router.post("/task_categories/")
def create_task_category(task_category_data: TaskCategoryCreate, session: Session = Depends(get_session)):
    task_category = TaskCategory(**task_category_data.dict())
    session.add(task_category)
    session.commit()
    session.refresh(task_category)
    return task_category


@router.get("/task_categories/", response_model=List[TaskCategory])
def read_task_categories(session: Session = Depends(get_session)):
    task_categories = session.query(TaskCategory).all()
    return task_categories


@router.get("/task_categories/{id}", response_model=List[TaskCategory])
def read_task_category(task_id: int, category_id: int, session: Session = Depends(get_session)):
    statement = select(TaskCategory).where(TaskCategory.task_id == task_id, TaskCategory.category_id == category_id)
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="TaskCategory not found")
    return results



@router.put("/task_categories/{task_id}/{category_id}", response_model=TaskCategoryUpdate)
def update_task_category(task_id: int, category_id: int, task_category_update: TaskCategory, session: Session = Depends(get_session)):
    db_task_category = session.get(TaskCategory, {'task_id': task_id, 'category_id': category_id})
    if not db_task_category:
        raise HTTPException(status_code=404, detail="TaskCategory not found")
    
    db_task_category.additional_info = task_category_update.additional_info

    session.commit()
    return db_task_category

```

## timelogs
```

router = APIRouter()

@router.post("/timelogs/", response_model=TimeLog)
def create_timelog(timelog: TimeLogCreate, session: Session = Depends(get_session)):  
    task = session.get(Task, timelog.task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {timelog.task_id} not found")

    db_timelog = TimeLog(**timelog.dict())  
    session.add(db_timelog)
    try:
        session.commit()
    except Exception as e:
        session.rollback()  
        raise HTTPException(status_code=400, detail=str(e))
    session.refresh(db_timelog)
    return db_timelog


@router.get("/timelogs/{timelog_id}", response_model=TimeLog)
def read_timelog(timelog_id: int, session: Session = Depends(get_session)):
    timelog = session.query(TimeLog).filter(TimeLog.id == timelog_id).first()
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    return timelog


@router.get("/timelogs/", response_model=List[TimeLog])
def read_timelogs(session: Session = Depends(get_session)):
    return session.query(TimeLog).all()

@router.put("/timelogs/{timelog_id}", response_model=TimeLog)
def update_timelog(timelog_id: int, timelog: TimeLogCreate, session: Session = Depends(get_session)):
    db_timelog = session.query(TimeLog).filter(TimeLog.id == timelog_id).first()
    if not db_timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    for var, value in vars(timelog).items():
        setattr(db_timelog, var, value) if value else None
    session.commit()
    session.refresh(db_timelog)  
    return db_timelog

@router.delete("/timelogs/{timelog_id}", response_model=dict)
def delete_timelog(timelog_id: int, session: Session = Depends(get_session)):
    timelog = session.get(TimeLog, timelog_id)
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    session.delete(timelog)
    session.commit()
    return {"ok": True}

```

## many-to-many, one-to-many
```
router = APIRouter()


@router.get("/categories/{category_id}/tasks", response_model=List[Task])
def read_tasks_by_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    tasks = session.query(Task).join(TaskCategory).filter(TaskCategory.category_id == category_id).all()
    return tasks

@router.get("/tasks/{task_id}/categories", response_model=List[Category])
def read_categories_by_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    categories = session.query(Category).join(TaskCategory).filter(TaskCategory.task_id == task_id).all()
    return categories

@router.get("/usersall/", response_model=List[UserWithTaskNames])
def read_users_with_tasks(session: Session = Depends(get_session)):
    statement = select(User).options(joinedload(User.tasks)).distinct()
    result = session.execute(statement)
    users = result.scalars().unique().all()
    users_with_task_names = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "tasks": [{"title": task.title} for task in user.tasks]
        }
        users_with_task_names.append(UserWithTaskNames(**user_data))

    return users_with_task_names
```