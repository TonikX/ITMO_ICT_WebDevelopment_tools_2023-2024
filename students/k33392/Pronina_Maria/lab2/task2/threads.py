import time
import threading
from parser import get_github_user_info as parse
from models import User, UserProject
from connection import get_session, init_db
from sqlalchemy.future import select


def parse_and_save(usernames, session):
    for username in usernames:
        data = parse(username)
        if data:
            user_prefs = ', '.join(str(pref) for pref in data['unique_languages'])
            save_user(data['name'], data['bio'], user_prefs, session)

            projects = data['pinned_repos']
            query = select(User).where(User.name == data['name'])
            user_id = session.exec(query).scalar().id
            save_projects(projects, user_id, session)


def save_user(name, about, preferences, session):
    print(f'User: \nName: {name} \nAbout: {about} \nPreferences: {preferences}')
    user = User(name=name, about=about, preferences=preferences)

    session.add(user)
    session.commit()


def save_projects(projects, user_id, session):
    for project in projects:
        cur_project = UserProject(user_id=user_id, name=project['repo_name'], description=project['about'])
        print(f'Project: \nUser: {user_id} \nName: {project["repo_name"]} \nDescription: {project["about"]}')

        session.add(cur_project)
        session.commit()


def main():
    usernames = ['berohomepc', 'FMyb', 'marypronina']
    session = next(get_session())

    n = 3
    chunk_size = len(usernames) // n
    chunks = list()
    for i in range(n):
        chunks.append(usernames[i * chunk_size:i * chunk_size + chunk_size])

    threads = list()
    for chunk in chunks:
        thread = threading.Thread(target=parse_and_save, args=(chunk, session))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    init_db()
    start_time = time.time()
    main()
    result_time = time.time() - start_time
    print(f'Time: {result_time}')
