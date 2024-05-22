import json

import psycopg2
import requests
from bs4 import BeautifulSoup


def get_connection():
    return psycopg2.connect(
        dbname="warriors_db",
        user="postgres",
        password="TecHeres3141",
        host="localhost",
        port="5432"
    )


def parse_and_save_users(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    users = []

    conn = get_connection()
    with conn.cursor() as cursor:
        for li in soup.select('ul > li'):
            user = {}
            username = li.select_one('.username').text
            password = li.select_one('.password').text
            profile_id = int(li.select_one('.profile-id').text)
            users.append(user)

            cursor.execute(
                "INSERT INTO \"user\" (username, password, profile_id) VALUES (%s, %s, %s)",
                (username, password, profile_id)
            )

    conn.commit()
    conn.close()

    print(f"Data from {url} parsed and saved to database.")


def parse_and_save_projects(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    projects = []

    conn = get_connection()

    cursor = conn.cursor()

    for li in soup.select('ul > li'):
        project = {}
        project_name = li.select_one('.name').text
        project_description = li.select_one('.description').text
        project_expected_result = li.select_one('.expected-result').text
        project_team_id = int(li.select_one('.team-id').text)
        projects.append(project)

        cursor.execute("INSERT INTO project (name, description, expected_result, team_id) VALUES (%s, %s, %s, %s)",
                       (project_name, project_description, project_expected_result, project_team_id))

    conn.commit()
    conn.close()
    print(f"Data from {url} parsed and saved to database.")


def parse_and_save_tasks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = get_connection()

    with conn.cursor() as cursor:
        for li in soup.select('ul > li'):
            task_name = li.select_one('.name').text
            task_description = li.select_one('.description').text
            task_deadline = li.select_one('.deadline').text
            project_id = int(li.select_one('.project-id').text)

            cursor.execute(
                "INSERT INTO task (name, description, deadline, project_id) VALUES (%s, %s, %s, %s)",
                (task_name, task_description, task_deadline, project_id)
            )

    conn.commit()
    conn.close()
    print(f"Data from {url} parsed and saved to database.")


def parse_and_save_userprofiles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = get_connection()

    with conn.cursor() as cursor:
        for li in soup.select('ul > li'):
            avatar = li.select_one('.avatar').text
            birth_date = li.select_one('.birth_date').text
            skills = [skill_li.text for skill_li in li.select('ol.skills > li')]

            cursor.execute(
                "INSERT INTO userprofile (avatar, birth_date, skills) VALUES (%s, %s, %s)",
                (avatar, birth_date, json.dumps(skills))
            )

    conn.commit()
    conn.close()
    print(f"Data from {url} parsed and saved to database.")


def parse_and_save_teams(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = get_connection()
    cursor = conn.cursor()

    for li in soup.select('ul > li'):
        team_name = li.select_one('.name').text

        cursor.execute(
            "INSERT INTO team (name) VALUES (%s)",
            (team_name,)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data from {url} parsed and saved to database.")


def parse_all_urls(handle_func, base, count):
    for i in range(1, count + 1):
        url = f"{base}{i}.html"
        handle_func(url)


data_handlers = {
    "tasks": parse_and_save_tasks,
    "projects": parse_and_save_projects,
    "users": parse_and_save_users,
    # "products": parse_and_save_products,
    "teams": parse_and_save_teams,
    # "carts": parse_and_save_carts,
    "userprofiles": parse_and_save_userprofiles,
}
