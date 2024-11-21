from fastapi import FastAPI
import typing
from enum import Enum
from pydantic import BaseModel

class Priority(Enum):
    low = 0
    medium = 1
    high = 2


class Project(BaseModel):
    title: str
    description: str


class CategoryBase(BaseModel):
    title: str
    description: str


class CategoryForm(CategoryBase):
    project_id:int


class CategoryFull(CategoryBase):
    project: Project


class Task(BaseModel):
    category: CategoryFull
    title: str
    description: str
    priority: Priority


projects = [Project(title='Main project', description='Something')]

categories = [CategoryFull(project=projects[0], title='cat1', description='desc1'),
              CategoryFull(project=projects[0], title='cat2', description='desc2')]

tasks = [Task(category=categories[0],title='task1', description='desc1', priority=Priority.low),
         Task(category=categories[1],title='task2', description='desc2', priority=Priority.medium)]

fake_db = {
    'projects': projects,
    'categories': categories,
    'tasks': tasks
}

app = FastAPI()


@app.get('/task/list/')
def get_tasks() -> typing.List[Task]:
    return fake_db['tasks']


@app.post('/project/add/')
def add_project(
    project: Project
) -> typing.TypedDict('response', {'status': int, 'data': Project}):
    return {'status': 200, 'data': project}


@app.post('/category/add/')
def add_category(
    category_form: CategoryForm
)-> typing.TypedDict('response', {'status': int, 'data': CategoryFull}):
    project_id = category_form.project_id
    category_dict = category_form.dict(exclude={'project_id'})
    category_dict['project'] = fake_db['projects'][project_id]
    category_full = CategoryFull(**category_dict)
    return {'status': 200, 'data': category_full}


if __name__ == '__main__':
    print(projects)