import requests
from bs4 import BeautifulSoup


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


# username = 'berohomepc'
# user_info = get_github_user_info(username)
# if user_info:
#     print(f"Name: {user_info['name']}")
#     print(f"Bio: {user_info['bio']}")
#     print(f"Skills: {', '.join(user_info['unique_languages'])}")
#     print("Pinned Repositories:")
#     for repo in user_info['pinned_repos']:
#         print(f"  - Name: {repo['repo_name']}")
#         print(f"    About: {repo['about']}")
#         print(f"    Language: {repo['language']}")
# else:
#     print("Не удалось получить информацию о пользователе")
