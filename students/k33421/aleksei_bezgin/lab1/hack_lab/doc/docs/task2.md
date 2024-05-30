# Task2

| approach        | mean time +- std (sec) |
|-----------------|------------------------|
| naive           | 20.01 +- 1.25          |
| threading       | 5.11 +- 0.95           |
| multiprocessing | 	4.0 +- 0.62           |
| asyncio         | 2.06 +- 1.64           |

Здесь использование threading уже оправдано, но multiprocessing все равно круче.
Выигрвывает же asyncio, однако, он же показывает наибольшую волатильность.

# Сниппеты кода

1. Наивная реализация
```commandline
def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    # спарсили данные про кейс
    inner_page = requests.get(hack_link)
    soup_in = BeautifulSoup(inner_page.text, 'html.parser')
    paragraphs = list(map(lambda x: x.text, soup_in.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            # пусть все хакатоны длятся неделю
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id  # Assign the hackathon_id to establish the relationship
        )
        session.add(task)
        session.commit()
        session.refresh(task)
```

2. multithreading
```commandline
def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    # спарсили данные про кейс
    inner_page = requests.get(hack_link)
    soup_in = BeautifulSoup(inner_page.text, 'html.parser')
    paragraphs = list(map(lambda x: x.text, soup_in.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            # пусть все хакатоны длятся неделю
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id  # Assign the hackathon_id to establish the relationship
        )
        session.add(task)
        session.commit()
        session.refresh(task)


def add_hackathon_list(hack_info_list):
    for hack_info in hack_info_list:
        add_hackathon(hack_info)


def main():
    hack_data = json.load(open('hack_links.json'))

    # используем несколько потоков
    num_threads = 5
    step = len(hack_data) // num_threads
    threads = []

    time_start = time.time()
    for i in range(num_threads):
        thread = threading.Thread(target=add_hackathon_list, args=(hack_data[i * step: (i + 1) * step], ))
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')
```

3. multiprocessing
```commandline
def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    # спарсили данные про кейс
    inner_page = requests.get(hack_link)
    soup_in = BeautifulSoup(inner_page.text, 'html.parser')
    paragraphs = list(map(lambda x: x.text, soup_in.find_all('p')))
    hack_case = '\n'.join(paragraphs)
    case_title = paragraphs[0]

    with Session(engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            # пусть все хакатоны длятся неделю
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        session.commit()
        session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id  # Assign the hackathon_id to establish the relationship
        )
        session.add(task)
        session.commit()
        session.refresh(task)


def add_hackathon_list(hack_info_list):
    for hack_info in hack_info_list:
        add_hackathon(hack_info)


def main():
    hack_data = json.load(open('hack_links.json'))

    # используем несколько потоков
    num_threads = 5
    step = len(hack_data) // num_threads
    processes = []

    time_start = time.time()
    for i in range(num_threads):
        process = multiprocessing.Process(target=add_hackathon_list, args=(hack_data[i * step: (i + 1) * step], ))
        process.start()
        processes.append(process)

    for p in processes:
        p.join()

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')
```

4. asyncio
```commandline
async def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    async with aiohttp.ClientSession() as session:
        async with session.get(hack_link) as response:
            inner_page = await response.text()
            soup_in = BeautifulSoup(inner_page, 'html.parser')
            paragraphs = [p.text for p in soup_in.find_all('p')]
            hack_case = '\n'.join(paragraphs)
            case_title = paragraphs[0]

    async with AsyncSession(async_engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        await session.commit()
        await session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)


async def add_hackathon_list(hack_info_list):
    tasks = [add_hackathon(hack_info) for hack_info in hack_info_list]
    await asyncio.gather(*tasks)


async def main():
    hack_data = json.load(open('hack_links.json'))

    num_threads = 5
    step = len(hack_data) // num_threads

    time_start = time.time()
    tasks = []
    for i in range(num_threads):
        task = add_hackathon_list(hack_data[i * step: (i + 1) * step])
        tasks.append(task)

    await asyncio.gather(*tasks)

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')
```