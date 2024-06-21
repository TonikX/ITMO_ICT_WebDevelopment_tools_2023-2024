import time
import asyncio
from async_parser import get_github_user_info as parse
from models import User, UserProject
from async_connection import get_session, init_db
from sqlalchemy.future import select


async def parse_and_save(usernames, session):
    for username in usernames:
        start_parse = time.time()
        data = await parse(username)
        result_parse = time.time() - start_parse
        print(f"Parsing {username} took {result_parse} seconds\n")

        if data:
            user_prefs = ', '.join(str(pref) for pref in data['unique_languages'])
            await save_user(data['name'], data['bio'], user_prefs, session)

            projects = data['pinned_repos']

            query = select(User).where(User.name == data['name'])
            data = await session.exec(query)
            user_id = data.scalar().id
            await save_projects(projects, user_id, session)


async def save_user(name, about, preferences, session):
    print(f'User: \nName: {name} \nAbout: {about} \nPreferences: {preferences}')
    user = User(name=name, about=about, preferences=preferences)
    session.add(user)
    await session.commit()


async def save_projects(projects, user_id, session):
    for project in projects:
        cur_project = UserProject(user_id=user_id, name=project['repo_name'], description=project['about'])
        print(f'Project: \nUser: {user_id} \nName: {project["repo_name"]} \nDescription: {project["about"]}')

        session.add(cur_project)
        await session.commit()


async def main():
    await init_db()
    usernames = ['FMyb', 'berohomepc', 'marypronina']
    session = await anext(get_session())

    n = 3
    chunk_size = len(usernames) // n
    chunks = list()
    for i in range(n):
        chunks.append(usernames[i * chunk_size:i * chunk_size + chunk_size])

    tasks = list()
    for chunk in chunks:
        task = asyncio.create_task(parse_and_save(chunk, session))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    result_time = time.time() - start_time
    print(f'Time: {result_time}')
