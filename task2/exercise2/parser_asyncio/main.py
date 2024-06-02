from dotenv import dotenv_values
from pathlib import Path
from notion_client import AsyncClient
from dataclasses import dataclass
from datetime import datetime
import models
from sqlalchemy import select
from db_connection import get_session_context
import asyncio
import requests
from elapsed_logging import logger
from uuid import UUID


exercise2_path = Path(__file__).parent.parent
env_path = exercise2_path / ".env"
config = dotenv_values(env_path)
notion_secret = config["notion_secret"]
db_id = "7401d3f130414235ab1abb429d41a31e"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM0NTQ4NzUsImlhdCI6MTcxNTQ1NDg3NSwic3ViIjoidXNlcjEifQ.u4I3i-utbj3gwwlLc9ABIfvKneg-Ri3VzZVkmoNh-Wc"
}


notion = AsyncClient(auth=notion_secret)


async def get_task_pages(db_id: str):
    """Получает все id страниц, которые находятся в БД

    Args:
        db_id (str): id БД в notion

    Returns:
        list[str]: Список id страниц
    """
    response = await notion.databases.query(db_id)
    entries_list = response["results"]
    page_ids = []
    for entry in entries_list:
        if entry["object"] == "page":
            page_id = entry["id"]
            page_ids.append(page_id)

    return page_ids

class TaskParser:
    def __init__(self, task_notion: dict) -> None:
        self.task_notion = task_notion
    
    
    def get_title(self) -> str | None:
        title_list = self.get_value_or_none(
            self.task_notion,
            ["Name", "title"]
        )
        if len(title_list) == 0:
            return None
        title_object = title_list[0]
        title = self.get_value_or_none(
            title_object,
            ['plain_text']
        )
        return title
    
    
    def get_category_title(self) -> str | None:
        title = self.get_value_or_none(
            self.task_notion, 
            ("Tasks", "select", "name")
        )
        return title
        
    def get_description(self) -> str | None:
        return None
    
    def get_deadline(self) -> str | None:
        deadline = self.get_value_or_none(
            self.task_notion, 
            ("due", "date", "start")
        )
        return deadline
        
    
    def get_priority(self) -> models.Priority | None:
        urgent_flag = self.get_value_or_none(
            self.task_notion,
            ['Urgent', 'checkbox']
        )
        if urgent_flag:
            return models.Priority.high
        return models.Priority.low
    
    def get_approximate_time(self) -> int | None:
        approximate_time = self.get_value_or_none(
            self.task_notion,
            ["Aproximate time", 'number']
        )
        if approximate_time is not None:
            approximate_time = int(approximate_time)
        return approximate_time
    
    @staticmethod
    def get_value_or_none(d, keys_tuple):
        for key in keys_tuple:
            if d is None:
                return None
            if key not in keys_tuple:
                return None
            
            d = d[key]
        return d

class TaskWriter: 
    def __init__(self, project_id, category_none_id) -> None:
        self.project_id = project_id
        self.category_none_id = category_none_id

    async def write_task_to_db(self, task_notion_id):
        task_notion = await notion.pages.retrieve(task_notion_id)
        task_notion = task_notion["properties"]
        task_notion = TaskParser(task_notion)

        if task_notion.get_title() is None:
            return

        async with get_session_context() as session:
            category_id = await self._get_category_id(session, task_notion)
            
            task_data = {
                "category_id": category_id,  # Будем заполнять ниже
                "title": task_notion.get_title(),
                "description": None,
                "deadline": task_notion.get_deadline(),
                "priority": task_notion.get_priority(),
                "approximate_time": task_notion.get_approximate_time(),
            }
            task_object = models.Task.model_validate(task_data)
            session.add(task_object)
            await session.commit()
            await session.refresh(task_object)


    async def _get_category_id(self, session, task_notion: TaskParser):
        category_title = task_notion.get_category_title()

        if category_title is None:
            return self.category_none_id

        # try to find category with that name
        category_obj = await self._find_category_obj(
            session,
            category_title,
        )

        if category_obj is None:
            category_obj = await self._create_category_obj(session, category_title)
        # Attribute error
        try:
            category_id = category_obj.id
        except AttributeError as e:
            print(category_obj)
            raise e
        return category_id

   

    async def _find_category_obj(self, session, category_title):
        query = (
            select(models.Category)
            .where(models.Category.title == category_title)
            .where(models.Category.project_id == self.project_id)
        )
        results = await session.exec(query)
        category_obj = results.first()
        if category_obj is not None:
            category_obj = category_obj[0]
        return category_obj

    async def _create_category_obj(self, session, category_title):
        category_data = {
            "project_id": self.project_id,
            "title": category_title,
            "description": None,
        }
        category_obj = models.Category.model_validate(category_data)
        session.add(category_obj)
        await session.commit()
        await session.refresh(category_obj)
        return category_obj

async def create_project():
    url = "http://127.0.0.1:13213/project/"
    json_data = {
        "title": "Notion tasks project async",
        "description": "Async notion tasks",
    }

    response = requests.post(url, headers=headers, json=json_data).json()
    project_id = response["object"]["id"]
    return project_id


async def create_none_category(project_id):
    url = f"http://127.0.0.1:13213/project/{project_id}/category/"
    json_data = {
        "title": "None category",
        "description": "If no category, it falls here",
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    category_id = response["object"]["id"]
    return category_id


async def main():
    logger.info("Начал выполнение")
    project_id = await create_project()
    category_none_id = await create_none_category(project_id)
    logger.info("Создал проект и none task")
    task_pages = await get_task_pages(db_id)
    logger.info("Получил id страниц тасков")
    task_writer = TaskWriter(project_id, category_none_id)
    async with asyncio.TaskGroup() as task_group:
        for task_id in task_pages:
            coroutine = task_writer.write_task_to_db(task_id)
            task_group.create_task(coroutine)
    logger.info("Собрал все данные и записал их в БД")



if __name__ == "__main__":
    logger.reset_time()
    asyncio.run(main())
