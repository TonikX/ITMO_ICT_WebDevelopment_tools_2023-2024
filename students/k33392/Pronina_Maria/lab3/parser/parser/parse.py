import requests
from bs4 import BeautifulSoup
from models import User, UserProject
from sqlalchemy.future import select

def get_github_user_info(username):
    url = f'https://github.com/{username}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        name_tag = soup.find('span', {'itemprop': 'name'})
        name = name_tag.get_text(strip=True)

        bio_tag = soup.find('div', {'class': 'p-note user-profile-bio mb-3 js-user-profile-bio f4'})
        bio = 'Не указано'
        if bio_tag:
            bio = bio_tag.get_text(strip=True)

        pinned_repos = soup.find_all('span', {'class': 'repo'})
        repo_info = []
        unique_languages = set()

        for repo in pinned_repos:
            repo_name = repo.get_text(strip=True)

            repo_url = f"https://github.com/{username}/{repo_name}"
            repo_response = requests.get(repo_url)

            if repo_response.status_code == 200:
                repo_soup = BeautifulSoup(repo_response.text, 'html.parser')

                language_tag = repo_soup.find('span', {'class': 'color-fg-default text-bold mr-1'})
                language = 'Не указано'
                if language_tag:
                    language = language_tag.get_text(strip=True)
                unique_languages.add(language)

                about_tag = repo_soup.find('p', {'class': 'f4 my-3'})
                about = 'Не указано'
                if about_tag:
                    about = about_tag.get_text(strip=True)

                repo_info.append({
                    'repo_name': repo_name,
                    'about': about,
                    'language': language
                })

        return {
            'name': name,
            'bio': bio,
            'unique_languages': list(unique_languages),
            'pinned_repos': repo_info
        }
    else:
        return None
    

def parse_and_save(usernames, session):
    for username in usernames:
        data = get_github_user_info(username)
        if data:
            user_prefs = ', '.join(str(pref) for pref in data['unique_languages'])
            save_user(username, data['name'], data['bio'], user_prefs, session)

            projects = data['pinned_repos']
            query = select(User).where(User.name == data['name'])
            user_id = session.exec(query).scalar().id
            save_projects(projects, user_id, session)


def save_user(username, name, about, preferences, session):
    print(f'User: \nName: {name} \nAbout: {about} \nPreferences: {preferences}')
    user = User(name=name, about=about, preferences=preferences, email=username, password='secret')

    print(user)
    session.add(user)
    session.commit()


def save_projects(projects, user_id, session):
    for project in projects:
        cur_project = UserProject(user_id=user_id, name=project['repo_name'], description=project['about'], in_search=False)
        print(f'Project: \nUser: {user_id} \nName: {project["repo_name"]} \nDescription: {project["about"]}')

        session.add(cur_project)
        session.commit()

