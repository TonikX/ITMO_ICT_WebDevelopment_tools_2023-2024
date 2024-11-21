from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from parser_threading import models
import requests
from parser_threading.db_connection import get_session_context
from dotenv import dotenv_values
from parser_threading.elapsed_logging import logger
from notion_client import Client
from parser_threading.category_manager import CategoryManager
from parser_threading.task_parser import TaskParser

import os

if "BACKEND_URL" not in os.environ:
    raise RuntimeError('enviromental variable "BACKEND_URL" is not set')
BACKEND_URL = os.environ["BACKEND_URL"]

exercise2_path = Path(__file__).parent
env_path = exercise2_path / ".env"
config = dotenv_values(env_path)
notion_secret = config["notion_secret"]
db_id = "7401d3f130414235ab1abb429d41a31e"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM0NTQ4NzUsImlhdCI6MTcxNTQ1NDg3NSwic3ViIjoidXNlcjEifQ.u4I3i-utbj3gwwlLc9ABIfvKneg-Ri3VzZVkmoNh-Wc"
}


notion = Client(auth=notion_secret)




def get_task_pages(db_id: str):
    """Получает все id страниц, которые находятся в БД

    Args:
        db_id (str): id БД в notion

    Returns:
        list[str]: Список id страниц
    """
    response = notion.databases.query(db_id)
    entries_list = response["results"]
    page_ids = []
    for entry in entries_list:
        if entry["object"] == "page":
            page_id = entry["id"]
            page_ids.append(page_id)

    return page_ids


class TaskWriter:
    def __init__(self, category_manager: CategoryManager) -> None:
        self.category_manager = category_manager

    def write_task_to_db(self, task_notion_id):
        task_notion = notion.pages.retrieve(task_notion_id)
        task_notion = task_notion["properties"]
        task_notion = TaskParser(task_notion)
        if task_notion.get_title() is None:
            return

        with get_session_context() as session:
            category_title = task_notion.get_category_title()
            category_id = self.category_manager.get_id(session, category_title)
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
            session.commit()
            session.refresh(task_object)


def create_project(headers):
    url =  f"{BACKEND_URL}/project/"
    json_data = {
        "title": "Notion tasks project threading",
        "description": "Threading notion tasks",
    }

    response = requests.post(url, headers=headers, json=json_data).json()
    project_id = response["object"]["id"]
    return project_id


def create_none_category(project_id, headers):
    url = f"{BACKEND_URL}/project/{project_id}/category/"
    json_data = {
        "title": "None category",
        "description": "If no category, it falls here",
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    category_id = response["object"]["id"]
    return category_id


def main(token):
    logger.reset_time()
    logger.info("Начал выполнение")
    
    headers = {
    "Authorization": f'Bearer {token}'
    }

    project_id = create_project(headers)
    category_none_id = create_none_category(project_id, headers)
    logger.info("Создал проект и none task")

    task_pages = get_task_pages(db_id)
    logger.info("Получил id страниц тасков")

    category_manager = CategoryManager(project_id, category_none_id)
    task_writer = TaskWriter(category_manager)
    with ThreadPoolExecutor() as executor:
        results = executor.map(task_writer.write_task_to_db, task_pages)
    try:
        for result in results:
            pass
    except Exception as e:
        print(e)
    logger.info("Собрал все данные и записал их в БД")


if __name__ == "__main__":
    main('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjU1MTE0NTQsImlhdCI6MTcxNzUxMTQ1NCwic3ViIjoidXNlcjEifQ.KFdmwPsRD5LKjmpDD64OJgf_velc7CfABsCaIqj2-2k')
