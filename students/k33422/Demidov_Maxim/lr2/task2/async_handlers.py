import json

import aiohttp
from bs4 import BeautifulSoup
import psycopg2
import asyncio
import aiopg

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def get_connection():
    # Настройки подключения к базе данных
    return await aiopg.connect(
        dsn="dbname=warriors_db user=postgres password=TecHeres3141 host=localhost port=5432"
    )


async def parse_and_save_users(session, url):
    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            for li in soup.select('ul > li'):
                username = li.select_one('.username').text
                password = li.select_one('.password').text
                profile_id = int(li.select_one('.profile-id').text)

                await cursor.execute(
                    "INSERT INTO \"user\" (username, password, profile_id) VALUES (%s, %s, %s)",
                    (username, password, profile_id)
                )
            await cursor.execute("COMMIT")

    print(f"Data from {url} parsed and saved to database.")


async def parse_and_save_projects(session, url):
    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            for li in soup.select('ul > li'):
                project_name = li.select_one('.name').text
                project_description = li.select_one('.description').text
                project_expected_result = li.select_one('.expected-result').text
                project_team_id = int(li.select_one('.team-id').text)

                await cursor.execute(
                    "INSERT INTO project (name, description, expected_result, team_id) VALUES (%s, %s, %s, %s)",
                    (project_name, project_description, project_expected_result, project_team_id))
            await cursor.execute("COMMIT")

    print(f"Data from {url} parsed and saved to database.")


async def parse_and_save_tasks(session, url):
    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            for li in soup.select('ul > li'):
                task_name = li.select_one('.name').text
                task_description = li.select_one('.description').text
                task_deadline = li.select_one('.deadline').text
                project_id = int(li.select_one('.project-id').text)

                await cursor.execute(
                    "INSERT INTO task (name, description, deadline, project_id) VALUES (%s, %s, %s, %s)",
                    (task_name, task_description, task_deadline, project_id)
                )

            await cursor.execute("COMMIT")

    print(f"Data from {url} parsed and saved to database.")


async def parse_and_save_userprofiles(session, url):
    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            for li in soup.select('ul > li'):
                avatar = li.select_one('.avatar').text
                birth_date = li.select_one('.birth_date').text
                skills = [skill_li.text for skill_li in li.select('ol.skills > li')]

                await cursor.execute(
                    "INSERT INTO userprofile (avatar, birth_date, skills) VALUES (%s, %s, %s)",
                    (avatar, birth_date, json.dumps(skills))
                )

            await cursor.execute("COMMIT")

    print(f"Data from {url} parsed and saved to database.")




async def parse_and_save_teams(session, url):
    async with session.get(url) as response:
        html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            for li in soup.select('ul > li'):
                team_name = li.select_one('.name').text

                await cursor.execute(
                    "INSERT INTO team (name) VALUES (%s)",
                    (team_name,)
                )

            await cursor.execute("COMMIT")

    print(f"Data from {url} parsed and saved to database.")


async def parse_all_urls(handler_func, base, count):
    async with aiohttp.ClientSession() as session:
        for i in range(1, count + 1):
            url = f"{base}{i}.html"
            try:
                await handler_func(session, url)
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(1)

data_handlers = {
    "tasks": parse_and_save_tasks,
    "projects": parse_and_save_projects,
    "users": parse_and_save_users,
    # "products": parse_and_save_products,
    "teams": parse_and_save_teams,
    # "carts": parse_and_save_carts,
    "userprofiles": parse_and_save_userprofiles,
}
