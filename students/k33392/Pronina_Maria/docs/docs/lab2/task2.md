# Задача 2


Задача: Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

## Реализация парсера
```python
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
```

##Реализация асинхронного парсера
```python
async def get_soup(url) -> BeautifulSoup:
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            return BeautifulSoup(await response.read(), "html.parser")


async def get_github_user_info(username):
    url = f'https://github.com/{username}'
    # if username == "berohomepc":
    #     await asyncio.sleep(2)

    start_time = time.time()
    soup = await get_soup(url)
    result_time = time.time() - start_time
    # print(f"Parsing {username} took {result_time} seconds\n")

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

        repo_url = f'https://github.com/{username}/{repo_name}'
        repo_soup = await(get_soup(repo_url))

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
```


##Результаты работы многопоточности
![](threading1.png)
![](threading2.png)

##Результаты работы многопроцессности
![](multiprocess1.png)
![](multiprocess2.png)

##Результаты работы асинхронности
![](async1.png)
![](async2.png)


## Выводы

Самое быстрое время показал асинхронный парсинг. Асинхронность действительно работает очень эффективно с запросами к веб сервисам и базам данных
Почти то же время показала и многопоточность.
Многопроцессность снова потратила очень много времени на создание процессов, из-за чего сильно проигрывает во времени.
